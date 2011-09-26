#!/usr/bin/env python

import tempfile
import shutil
import zipfile
from optparse import OptionParser

from django.db import transaction

from traveldash.gtfs.models import *

def main():
    parser = OptionParser()
    parser.add_option("--source", action="store", dest="source_id", type="int", metavar="SOURCE_ID", help="ID of a Source object to relate the imported data to")
    
    options,args = parser.parse_args()
    if not len(args) == 1:
        parser.error("Need to specify exactly one zip file")

    if options.source_id:
        source = Source.objects.get(pk=options.source_id)
    else:
        source = None

    loader = transaction.commit_on_success(load_zip)
    loader(args[0], source)

def load_zip(zip_file, source):
    temp_dir = tempfile.mkdtemp()
    try:
        print('Extracting %s...' % zip_file)
        zip = zipfile.ZipFile(open(zip_file, 'rb'))
        zip.extractall(temp_dir)

        load(temp_dir, source)
    finally:
        shutil.rmtree(temp_dir)

def load(temp_dir, source):
    # load GTFS data files & transform/derive additional data
    # due to foreign key constraints these files need to be loaded in the appropriate order
    Agency.gtfs_load(source, temp_dir)
    Calendar.gtfs_load(source, temp_dir)
    CalendarDate.gtfs_load(source, temp_dir)
    Route.gtfs_load(source, temp_dir)
    Stop.gtfs_load(source, temp_dir)
    Transfer.gtfs_load(source, temp_dir)
    Shape.gtfs_load(source, temp_dir)
    Trip.gtfs_load(source, temp_dir)
    StopTime.gtfs_load(source, temp_dir)
    Frequency.gtfs_load(source, temp_dir)
    Fare.gtfs_load(source, temp_dir)
    FareRule.gtfs_load(source, temp_dir)

    # Calculated/Derived stuff
    UniversalCalendar.gtfs_rebuild(source)

if __name__ == '__main__':
    main()
