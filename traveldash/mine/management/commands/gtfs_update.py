import os
import getpass
import urllib
import urllib2
import tempfile
from datetime import datetime

from django.core.management.base import BaseCommand, make_option, CommandError
from django.db import transaction
from django.conf import settings

from traveldash.mine.models import GTFSSource, Dashboard


class Command(BaseCommand):
    help = "Updates GTFS data. Specify either --all, --auto, --google-fusion-only, or a specific source/zip"
    args = "[SOURCE_ID [ZIP]]"
    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            default=False,
            help='Update all updateable sources (whether they need it or not)'),
        make_option('--auto',
            action='store_true',
            default=False,
            help='Update all the sources that need it as per their schedules'),
        make_option('--google-fusion',
            action='store_true',
            default=False,
            help='Update only the Google Fusion Table'),
        )

    def handle(self, *args, **options):
        if (len(args) and (options['all'] or options['auto'] or options['google_fusion'])) \
                or sum([options['all'], options['auto'], options['google_fusion']]) > 1 \
                or (sum([options['all'], options['auto'], options['google_fusion']]) == 0 and not len(args)):
            raise CommandError("Invalid combination of options")

        if options['google_fusion']:
            self.update_fusion_tables()
            return

        temp_files = []

        sources = []
        qs = None
        if len(args):
            try:
                source_id = int(args[0])
                source = GTFSSource.objects.get(pk=source_id)
            except:
                raise CommandError("Couldn't find source %s" % args[0])

            if len(args) > 1:
                zip_file = args[1]
                if not os.path.exists(args[1]):
                    raise CommandError("zip file not found")
                sources = [(source, zip_file)]
            else:
                qs = [source]
                if not source.can_autoupdate:
                    raise CommandError("Source %s (%s) can't auto-update, you need to manually specify a ZIP path" % (source, source_id))
        else:
            if options['all']:
                qs = GTFSSource.objects.updateable()
            elif options['auto']:
                qs = GTFSSource.objects.need_update()

            if not qs:
                print "No sources to update"
                return

        if qs:
            for source in qs:
                zip_fd = tempfile.NamedTemporaryFile(suffix='.zip')
                temp_files.append(zip_fd)
                source.download_zip(zip_fd)
                sources.append((source, zip_fd.name))

        self.update_models(sources)
        self.update_fusion_tables()

        print "All done :)"

    @transaction.commit_on_success
    def update_models(self, source_info):
        from traveldash.mine.models import DashboardRoute
        from traveldash.gtfs import load

        print "Unlinking dashboard stops..."
        DashboardRoute.objects.unlink_stops()

        # do the load
        for source, zip_file in source_info:
            print "Updating source %s from %s ..." % (source, zip_file)
            load.load_zip(zip_file, source)
            source.last_update = datetime.now()
            source.save()

        print "Re-linking dashboard stops..."
        DashboardRoute.objects.relink_stops()

        unlinked = DashboardRoute.objects.unlinked_stops()
        if len(unlinked):
            print "WARNING: UNLINKED DASHBOARDS"
            for d in Dashboard.objects.filter(pk__in=unlinked.values_list('dashboard__id')):
                print d.id, d

    def update_fusion_tables(self):
        from traveldash.gtfs.models import Stop

        print "Updating Google Fusion Tables..."

        user_auth_file = os.path.expanduser('~/.traveldash_auth')
        if os.path.exists(user_auth_file):
            print "Using credentials from %s" % user_auth_file
            with open(user_auth_file) as fa:
                g_username, g_password = fa.readline().strip().split(':', 1)
        else:
            g_username = raw_input('Google Account Email: ')
            g_password = getpass.getpass('Password: ')

        req = {
            'Email': g_username,
            'Passwd': g_password,
            'accountType': 'HOSTED_OR_GOOGLE',
            'service': 'fusiontables',
            'source': 'traveldash.org-backend-0.1',
        }
        print "Logging in..."
        for line in urllib2.urlopen('https://www.google.com/accounts/ClientLogin', urllib.urlencode(req)):
            if line.startswith('Auth='):
                g_auth = line[5:].strip()
                break
        else:
            raise CommandError("Didn't get auth token from Google")

        print "Generating data...",
        inserts = []
        for id, name, location in Stop.objects.get_fusion_tables_rows():
            inserts.append("INSERT INTO %s (id, name, location) VALUES (%s, '%s', '%s');" % (settings.GTFS_STOP_FUSION_TABLE_ID, id, name.replace("'", "\\'"), location))
        print len(inserts)

        print "Truncating table..."
        req_data = {
            'sql': 'DELETE FROM %s' % settings.GTFS_STOP_FUSION_TABLE_ID,
        }
        req = urllib2.Request("https://www.google.com/fusiontables/api/query", urllib.urlencode(req_data), headers={'Authorization': 'GoogleLogin auth=%s' % g_auth})
        urllib2.urlopen(req)

        print "Adding new rows..."
        for j, chunk in enumerate([inserts[i: i + 500] for i in range(0, len(inserts), 500)]):
            print "  %d-%d..." % (j * 500 + 1, (j + 1) * 500)
            req_data = {
                'sql': '\n'.join(chunk),
            }
            req = urllib2.Request("https://www.google.com/fusiontables/api/query", urllib.urlencode(req_data), headers={'Authorization': 'GoogleLogin auth=%s' % g_auth})
            try:
                urllib2.urlopen(req)
            except urllib2.HTTPError, e:
                print "GFT Error: %s\nInsert Data:\n" % e
                for i, line in enumerate(req_data['sql'].split('\n')):
                    print '%d\t%s' % (i, line)
                raise

        print "All done :)"
