import os

from django.core.management.base import BaseCommand, make_option, CommandError
from django.db import transaction

class Command(BaseCommand):
    help = "Updates GTFS data from a zip file"
    args = "ZIP"
    
    def handle(self, *args, **options):
        if len(args) != 1 or not os.path.exists(args[0]):
            raise CommandError("zip file not found")
            
        self.do_it(args[0])

    @transaction.commit_on_success
    def do_it(self, zip_file):
        from traveldash.mine.models import DashboardRoute
        from traveldash.gtfs import load
        
        print "Unlinking dashboard stops..."
        DashboardRoute.objects.unlink_stops()
        
        # do the load
        load.load_zip(zip_file, None)
        
        print "Re-linking dashboard stops..."
        DashboardRoute.objects.relink_stops()

        print "All done :)"
