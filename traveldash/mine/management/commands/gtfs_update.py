import os
import getpass
import urllib
import urllib2
import tempfile
from datetime import datetime
import logging
import time

import requests
from django.core.management.base import BaseCommand, make_option, CommandError
from django.db import transaction
from django.conf import settings

from traveldash.mine.models import GTFSSource, Dashboard


class Command(BaseCommand):
    L = logging.getLogger("traveldash.mine.gtfs_update")

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

        # configure logging output
        if options['verbosity'] == '0':
            log_level = logging.WARNING
        elif options['verbosity'] == '1':
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        logging.basicConfig(stream=self.stderr, level=log_level, format="%(relativeCreated)s %(name)s[%(levelname)s]: %(message)s")

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
                    raise CommandError("ZIP file not found")
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
                self.L.info("No sources to update")
                return

        if qs:
            for source in qs:
                zip_fd = tempfile.NamedTemporaryFile(suffix='.zip')
                temp_files.append(zip_fd)
                source.download_zip(zip_fd)
                sources.append((source, zip_fd.name))

        self.update_models(sources)
        self.update_fusion_tables()

        self.L.info("All done :)")

    @transaction.commit_on_success
    def update_models(self, source_info):
        from traveldash.mine.models import DashboardRoute
        from traveldash.gtfs import load

        self.L.info("Unlinking dashboard stops...")
        DashboardRoute.objects.unlink_stops()

        # do the load
        for source, zip_file in source_info:
            self.L.info("Updating source %s from %s ...", source, zip_file)
            load.load_zip(zip_file, source)
            source.last_update = datetime.now()
            source.save()

        self.L.info("Re-linking dashboard stops...")
        errors = DashboardRoute.objects.relink_stops(ignore_errors=True)
        if len(errors):
            self.L.error("ERRORS RELINKING STOPS:\n%s", "\n".join(map(str, errors)))

        unlinked = DashboardRoute.objects.unlinked_stops()
        if len(unlinked):
            pk_list = Dashboard.objects.filter(pk__in=unlinked.values_list('dashboard__id')).values_list('pk', flat=True)
            self.L.warning("WARNING: UNLINKED DASHBOARDS: %s", pk_list)

    def update_fusion_tables(self):
        import httplib2
        from apiclient.discovery import build
        from oauth2client.client import SignedJwtAssertionCredentials

        from traveldash.gtfs.models import Stop

        FUSION_BASE_URL = "https://www.googleapis.com/fusiontables/v1"

        self.L.info("Updating Google Fusion Tables...")

        user_auth_file = os.path.expanduser('~/.traveldash_auth.p12')
        with open(user_auth_file, 'rb') as f:
            key = f.read()

        #FUSION_TABLES_API_EMAIL = '425751465297-lmvpl2m4luql9p630lfta55vcvbq52ad@developer.gserviceaccount.com'
        FUSION_TABLES_API_EMAIL = '1010325034106-jdop1gjin0n75hkomdjc3mksir3e3l57@developer.gserviceaccount.com'
        credentials = SignedJwtAssertionCredentials(FUSION_TABLES_API_EMAIL,
                                                    key,
                                                    scope='https://www.googleapis.com/auth/fusiontables')
        http = httplib2.Http()
        credentials.authorize(http)
        # service = build("fusiontables", "v1", http=http)

        headers = {
            'Authorization': 'Bearer %s' % credentials.access_token,
        }

        self.L.info("Generating data...",)
        inserts = []
        for id, name, location in Stop.objects.get_fusion_tables_rows():
            inserts.append("INSERT INTO %s (id, name, location) VALUES (%s, '%s', '%s');" % (settings.GTFS_STOP_FUSION_TABLE_ID, id, name.replace("'", "\\'"), location))
        self.L.info("%s rows to insert", len(inserts))

        # self.L.info("Truncating table...")
        # req_data = {
        #     'sql': 'DELETE FROM %s;' % settings.GTFS_STOP_FUSION_TABLE_ID
        # }
        # r = requests.post(FUSION_BASE_URL + "/query", data=req_data, headers=headers)
        # self.L.debug(r.text)
        # r.raise_for_status()

        # self.L.info("Sleeping for 15 seconds...")
        # time.sleep(15)

        self.L.info("Adding new rows...")
        N = 10
        for j, chunk in enumerate([inserts[i: i + N] for i in range(0, len(inserts), N)]):
            self.L.info("  %d-%d..." % (j * N + 1, (j + 1) * N))
            req_data = {
                'sql': '\n'.join(chunk),
            }
            try:
                #r = requests.post(FUSION_BASE_URL + "/query?key=%s" % FUSION_TABLES_KEY, data=req_data)
                r = requests.post(FUSION_BASE_URL + "/query", data=req_data, headers=headers)
                # print(service.query().sql(sql=req_data['sql']).execute())
                self.L.debug(r.text)
                r.raise_for_status()
            except (requests.HTTPError, requests.exceptions.RequestException):
                sql_data = []
                for i, line in enumerate(req_data['sql'].split('\n')):
                    sql_data.append('%d\t%s' % (i, line))
                self.L.error("GFT Error: Insert Data:\n%s", "\n".join(sql_data), exc_info=True)
                raise

        self.L.info("All done :)")
