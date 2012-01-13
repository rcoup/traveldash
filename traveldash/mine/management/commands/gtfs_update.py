import os
import tempfile
import getpass
import urllib
import urllib2

from django.core.management.base import BaseCommand, make_option, CommandError
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    help = "Updates GTFS data from a zip file"
    args = "ZIP"

    def handle(self, *args, **options):
        if len(args) != 1 or not os.path.exists(args[0]):
            raise CommandError("zip file not found")

        self.update_models(args[0])

        print "Updating Google Fusion Tables..."
        self.update_fusion_tables()

        print "All done :)"

    @transaction.commit_on_success
    def update_models(self, zip_file):
        from traveldash.mine.models import DashboardRoute
        from traveldash.gtfs import load

        print "Unlinking dashboard stops..."
        DashboardRoute.objects.unlink_stops()

        # do the load
        load.load_zip(zip_file, None)

        print "Re-linking dashboard stops..."
        DashboardRoute.objects.relink_stops()

    def update_fusion_tables(self):
        from traveldash.gtfs.models import Stop

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

        print "Generating data..."
        inserts = []
        for id, name, location in Stop.objects.get_fusion_tables_rows():
            inserts.append("INSERT INTO %s (id, name, location) VALUES (%s, '%s', '%s');" % (settings.GTFS_STOP_FUSION_TABLE_ID, id, name, location))

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
            urllib2.urlopen(req)

        print "All done :)"
