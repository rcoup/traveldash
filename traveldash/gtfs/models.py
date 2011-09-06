import time
import os
import codecs
import csv
import re
import datetime

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model

class GTFSModel(object):
    """ Loading behaviour for GTFS files """
    
    class UTF8Recoder(object):
        """ Iterator that reads an encoded stream and reencodes the input to UTF-8 """
        def __init__(self, f, encoding):
            self.reader = codecs.getreader(encoding)(f)
    
        def __iter__(self):
            return self
    
        def next(self):
            return self.reader.next().encode('utf-8')
 
    @classmethod
    def gtfs_load(cls, source, directory):
        print "%s..." % cls.__name__
        print '  %s' % cls.gtfs_filename()
        file_path = os.path.join(directory, cls.gtfs_filename())
        if not os.path.exists(file_path):
            print "  not found"
        else:
            cls._gtfs_relation_cache = {}
            try:
                start_time = time.time()
                with open(file_path, 'r') as f:
                    utf8_file = GTFSModel.UTF8Recoder(f, 'utf-8-sig')
                    reader = csv.DictReader(utf8_file)
    
                    cls.gtfs_truncate(source)
    
                    for i, o in enumerate(cls.gtfs_generate(source, reader)):
                        o.save()
    
                processing_time = time.time() - start_time
                print '  %d records, %.0f seconds' % (i+1, processing_time)
            finally:
                del cls._gtfs_relation_cache
    
    @classmethod
    def gtfs_truncate(cls, source):
        # truncate existing records
        if 'source' in cls._meta.get_all_field_names():
            cls.objects.filter(source=source).delete()
        else:
            cls.objects.all().delete()
    
    @classmethod
    def gtfs_filename(cls):
        if hasattr(cls, 'GTFS_FILENAME'):
            return cls.GTFS_FILENAME

        # convert ModelName to model_name.txt
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        if not s2.endswith('s'):
            s2 += 's'
        return "%s.txt" % s2

    @classmethod
    def gtfs_generate(cls, source, reader):
        for row in reader:
            yield cls.gtfs_instantiate(source, row)
    
    @classmethod
    def gtfs_instantiate(cls, source, row):
        o = cls()

        if 'source' in cls._meta.get_all_field_names():
            setattr(o, 'source', source)

        matched = []
        errors = []
        for k,v in row.items():
            if isinstance(v, basestring):
                v = v.strip()
            if k.endswith('date'):
                v = datetime.datetime.strptime(v, '%Y%m%d').date()
            
            if k in cls._meta.get_all_field_names():
                # normal field
                try:
                    if isinstance(cls._meta.get_field_by_name(k)[0], models.BooleanField):
                        # '0' ends up as True...
                        v = int(v)

                    setattr(o, k, v)
                except ValueError, e:
                    # will leave it to be sorted by gtfs_populate()
                    errors.append(e)
                else:
                    matched.append(k)
            elif k.endswith('_id'):
                # FK reference
                kk = k.rsplit('_', 1)[0]
                if v and (kk in cls._meta.get_all_field_names()):
                    try:
                        setattr(o, k, cls.gtfs_lookup_ref(k, kk, v, source))
                    except (ValueError, ObjectDoesNotExist), e:
                        # will leave it to be sorted by gtfs_populate()
                        errors.append(e)
                    else:
                        matched.append(k)
            elif k.startswith(cls.__name__.lower() + "_"):
                # dumb prefix
                kk = k.split('_', 1)[1]
                if kk in cls._meta.get_all_field_names():
                    setattr(o, kk, v or cls._meta.get_field_by_name(kk)[0].default)
                    matched.append(k)

        matched += cls.gtfs_populate(o, row, source)

        unmatched = set(row.keys()).difference(set(matched))
        if len(unmatched):
            raise ValueError("%s: Found unmatched CSV columns: %s (matched %s) (errors=%s)" % (cls.__name__, ', '.join(unmatched), ', '.join(set(matched)), errors))

        return o

    @classmethod
    def gtfs_populate(cls, o, row, source):
        # Override in subclasses to do calculated fields or other useful population of model
        # instance o from CSV row. Must return the source CSV fieldnames that it consumes.
        return ()

    @classmethod
    def gtfs_parse_hms(cls, v):
        if v == '': return None
        h, m, s = map(int, v.split(':'))
        return h*3600 + m*60 + s

    @classmethod
    def gtfs_parse_hms_days(cls, v):
        secs = cls.gtfs_parse_hms(v)
        if secs is not None:
            days = secs / 86400
            secs = secs - days * 86400
        else:
            days = None
        return secs, days

    @classmethod
    def gtfs_lookup_ref(cls, reference, model_name, value, source):
        """
        Do FK lookups on relations. Return the PK of the related instance
        reference: (eg. stop_id)
        model_name: relation (eg. stop)
        value: value of reference field on the relation (eg. STOP123ZZ)
        source: source dataset instance
        """
        cache_key = (reference, source, value)
        pk = cls._gtfs_relation_cache.get(cache_key)
        if pk is None:
            model_class = get_model('gtfs', model_name)
            query = {reference: value}
            if 'source' in cls._meta.get_all_field_names():
                query['source'] = source
    
            pk = model_class.objects.get(**query).pk
            cls._gtfs_relation_cache[cache_key] = pk
        return pk

if settings.GTFS_SOURCE_MODEL == "gtfs.Source":
    class Source(models.Model):
        name = models.CharField(max_length=200)
    
        def __unicode__(self):
            return unicode(self.name)

class Agency(models.Model, GTFSModel):
    GTFS_FILENAME = 'agency.txt'

    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    agency_id = models.CharField(max_length=20, db_index=True)
    name = models.TextField()
    url = models.URLField()
    timezone = models.CharField(max_length=40)
    lang = models.CharField(max_length=2)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Agencies"
        unique_together = (("source", "agency_id"))

    def __unicode__(self):
        return unicode(self.name)

class Stop(models.Model, GTFSModel):
    LOCATION_TYPES = (
        (0, "Stop"),
        (1, "Station"),
    )
    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    stop_id = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=200, db_index=True)
    name = models.TextField()
    desc = models.TextField()
    location = models.PointField(geography=True)
    zone = models.ForeignKey('Zone', null=True, related_name='stops')
    url = models.URLField()
    location_type = models.IntegerField(choices=LOCATION_TYPES, default=0, db_index=True)
    parent_station = models.ForeignKey('self', null=True, related_name='child_stops')

    objects = models.GeoManager()

    class Meta:
        unique_together = (("source", "stop_id"))

    @classmethod
    def gtfs_populate(cls, o, row, source):
        o.location = geos.Point(float(row['stop_lon']), float(row['stop_lat']))

        if row.get('zone_id'):
            try:
                o.zone = Zone.objects.get(zone_id=row['zone_id'])
            except Service.DoesNotExist:
                o.zone = Zone.objects.create(source=source, zone_id=row['zone_id'])

        return ('stop_lon', 'stop_lat', 'zone_id',)


    def __unicode__(self):
        if self.code:
            return u"%s: %s" % (self.code, self.name)
        else:
            return unicode(self.name)

class RouteManager(models.Manager):
    def between_stops(self, from_stop, to_stop):
        """ Return all the Routes running between the specified stops """
        trips = Trip.objects.between_stops(from_stop, to_stop)
        return self.get_query_set().filter(trips__in=trips).distinct()

class Route(models.Model, GTFSModel):
    TRAM = 0
    SUBWAY = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_CAR = 5
    GONDOLA = 6
    FURNICULAR = 7
    ROUTE_TYPES = (
        (TRAM, "Tram, Streetcar, Light rail"),
        (SUBWAY, "Subway, Metro"),
        (RAIL, "Rail"),
        (BUS, "Bus"),
        (FERRY, "Ferry"),
        (CABLE_CAR, "Cable car"),
        (GONDOLA, "Gondola, Suspended cable car"),
        (FURNICULAR, "Funicular"),
    )
    route_id = models.CharField(max_length=20, db_index=True)
    agency = models.ForeignKey('Agency', null=True, related_name='routes')
    short_name = models.CharField(max_length=200, db_index=True)
    long_name = models.TextField()
    desc = models.TextField(blank=True)
    route_type = models.IntegerField(choices=ROUTE_TYPES, db_index=True)
    url = models.URLField(max_length=1000, blank=True)
    color = models.CharField(max_length=6, blank=True)
    text_color = models.TextField(max_length=6, blank=True)

    objects = RouteManager()

    class Meta:
        unique_together = (("agency", "route_id"))

    def __unicode__(self):
        return u"%s: %s %s" % (self.get_route_type_display(), self.short_name, self.long_name)

class Block(models.Model, GTFSModel):
    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    block_id = models.TextField(max_length=20, db_index=True)

    class Meta:
        unique_together = (("source", "block_id"))

    def __unicode__(self):
        return unicode(self.block_id)

class TripManager(models.Manager):
    def between_stops(self, from_stop, to_stop):
        """ Return all the Trips running between the specified stops """
        qs = self.get_query_set().filter(stop_times__stop=from_stop, stop_times__pickup_type=StopTime.PICKUP)
        qs = qs.filter(stop_times__stop=to_stop, stop_times__dropoff_type=StopTime.DROPOFF)
        return qs.distinct()
    
    def for_dates(self, *dates):
        return self.get_query_set().filter(service__all_dates__date__in=dates)

class Trip(models.Model, GTFSModel):
    OUTBOUND = 0
    INBOUND = 1
    DIRECTIONS = (
        (OUTBOUND, 'Outbound'),
        (INBOUND, 'Inbound'),
    )
    trip_id = models.CharField(max_length=100, db_index=True)
    route = models.ForeignKey('Route', related_name='trips')
    service = models.ForeignKey('Service', related_name='trips')
    headsign = models.TextField()
    short_name = models.TextField()
    direction_id = models.IntegerField(null=True, choices=DIRECTIONS, db_index=True)
    block = models.ForeignKey('Block', null=True, related_name='trips')
    shape = models.ForeignKey('Shape', null=True, related_name='trips')

    objects = TripManager()

    class Meta:
        unique_together = (("service", "trip_id"), ("route", "trip_id"))
        
    @property
    def is_outbound(self):
        return self.direction_id == self.OUTBOUND

    @property
    def is_inbound(self):
        return self.direction_id == self.INBOUND

    def __unicode__(self):
        return u"%s %s (%s)" % (self.route, self.get_direction_id_display(), self.service.service_id)

class StopTime(models.Model, GTFSModel):
    PICKUP = 0
    DROPOFF = 0
    DROPOFF_TYPES = (
        (DROPOFF, "Regularly scheduled drop off"),
        (1, "No drop off available"),
        (2, "Must phone agency to arrange drop off"),
        (3, "Must coordinate with driver to arrange drop off"),
    )
    PICKUP_TYPES = (
        (PICKUP, "Regularly scheduled pickup"),
        (1, "No pickup available"),
        (2, "Must phone agency to arrange pickup"),
        (3, "Must coordinate with driver to arrange pickup"),
    )
    
    trip = models.ForeignKey('Trip', related_name='stop_times')
    arrival_time = models.IntegerField(null=True)
    arrival_days = models.IntegerField(null=True)
    departure_time = models.IntegerField(null=True)
    departure_days = models.IntegerField(null=True)
    stop = models.ForeignKey('Stop', related_name='times')
    stop_sequence = models.IntegerField()
    stop_headsign = models.TextField()
    pickup_type = models.IntegerField(choices=PICKUP_TYPES, default=PICKUP)
    drop_off_type = models.IntegerField(choices=DROPOFF_TYPES, default=DROPOFF)
    shape_dist_travelled = models.FloatField(null=True)

    @classmethod
    def gtfs_populate(cls, o, row, source):
        o.arrival_time, o.arrival_days = cls.gtfs_parse_hms_days(row['arrival_time'])
        o.departure_time, o.departure_days = cls.gtfs_parse_hms_days(row['departure_time'])
        return ('arrival_time', 'departure_time')

    class Meta:
        ordering = ('trip', 'stop_sequence')

    def __unicode__(self):
        return u"%s: %s: %s" % (self.trip, self.stop, self.departing())

    def departing(self, service_date=None):
        if service_date is None:
            return datetime.time(self.departure_time / 3600, self.departure_time % 3600 / 60, self.departure_time % 60)
        dt = datetime.datetime(service_date.year, service_date.month, service_date.day, 12, 0, 0)
        dt -= datetime.timedelta(hours=12)
        dt += datetime.timedelta(seconds=self.departure_time, days=self.departure_days)
        return dt

    def arriving(self, service_date=None):
        if service_date is None:
            return datetime.time(self.arrival_time / 3600, self.arrival_time % 3600 / 60, self.arrival_time % 60)
        dt = datetime.datetime(service_date.year, service_date.month, service_date.day, 12, 0, 0)
        dt -= datetime.timedelta(hours=12)
        dt += datetime.timedelta(seconds=self.arrival_time, days=self.arrival_days)
        return dt

class Service(models.Model, GTFSModel):
    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    service_id = models.TextField(max_length=20, db_index=True)

    class Meta:
        unique_together = (("source", "service_id"))

    def __unicode__(self):
        return unicode(self.service_id)
    
class Calendar(models.Model, GTFSModel):
    GTFS_FILENAME = 'calendar.txt'

    service = models.OneToOneField('Service')
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

    @classmethod
    def gtfs_populate(cls, o, row, source):
        try:
            o.service = Service.objects.get(service_id=row['service_id'])
        except Service.DoesNotExist:
            o.service = Service.objects.create(source=source, service_id=row['service_id'])
        return ('service_id',)
    
    def __unicode__(self):
        return u"%s (%s to %s)" % (self.service.service_id, self.start_date, self.end_date)

    @property
    def weekdays(self):
        days = []
        for index,weekday in enumerate(('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')):
            if getattr(self, weekday):
                days.append(index)
        return tuple(days)

    def get_dates(self):
        d = self.start_date
        delta = datetime.timedelta(days=1)
        weekdays = set(self.weekdays)
        while d <= self.end_date:
            if d.weekday() in weekdays:
                yield d
            d += delta

class CalendarDate(models.Model, GTFSModel):
    ADDED = 1
    REMOVED = 2
    EXCEPTION_TYPES = (
        (ADDED, "Service added"),
        (REMOVED, "Service removed"),
    )
    service = models.ForeignKey('Service', related_name='calendar_exceptions')
    date = models.DateField()
    exception_type = models.IntegerField(choices=EXCEPTION_TYPES, db_index=True)

    @classmethod
    def gtfs_populate(cls, o, row, source):
        try:
            o.service = Service.objects.get(service_id=row['service_id'])
        except Service.DoesNotExist:
            o.service = Service.objects.create(source=source, service_id=row['service_id'])
        return ('service_id',)

    def __unicode__(self):
        return u"%s (%s): %s" % (self.service.service_id, self.date, self.get_exception_type_display())
    
    @property
    def is_added(self):
        return self.exception_type == self.ADDED

    @property
    def is_removed(self):
        return self.exception_type == self.REMOVED

class Fare(models.Model, GTFSModel):
    GTFS_FILENAME = 'fare_attributes.txt'
    PAYMENT_METHODS = (
        (0, "Fare is paid on board"),
        (1, "Fare must be paid before boarding"),
    )
    TRANSFERS = (
        (None, "Unlimited transfers are permitted."),
        (0, "No transfers permitted on this fare."),
        (1, "Passenger may transfer once."),
        (2, "Passenger may transfer twice."),
    )
    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    fare_id = models.CharField(max_length=20, db_index=True)
    price = models.FloatField()
    currency_type = models.CharField(max_length=3)
    payment_method = models.IntegerField(choices=PAYMENT_METHODS)
    transfers = models.IntegerField(choices=TRANSFERS, null=True)
    transfer_duration = models.IntegerField()

    class Meta:
        unique_together = (("source", "fare_id"))

class FareRule(models.Model, GTFSModel):
    fare = models.ForeignKey('Fare', related_name='rules')
    route = models.ForeignKey('Route', null=True, related_name='fare_rules')
    origin = models.ForeignKey('Zone', null=True, related_name="fare_rule_origins")
    destination = models.ForeignKey('Zone', null=True, related_name="fare_rule_destinations")
    contains = models.ForeignKey('Zone', null=True, related_name="fare_rule_contains")

    @classmethod
    def gtfs_populate(cls, o, row, source):
        for k in ('origin_id', 'destination_id', 'contains_id'):
            f = k.split('_')[0]
            if row.get(k):
                try:
                    setattr(o, f, Zone.objects.get(zone_id=row[k]))
                except Zone.DoesNotExist:
                    setattr(o, f, Zone.objects.create(source=source, zone_id=row[k]))

        return ('origin_id', 'destination_id', 'contains_id')

class Zone(models.Model, GTFSModel):
    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    zone_id = models.TextField(max_length=20, db_index=True)

    class Meta:
        unique_together = (("source", "zone_id"))

class Shape(models.Model, GTFSModel):
    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
    shape_id = models.CharField(max_length=20, db_index=True)
    path = models.LineStringField(geography=True, null=True)

    objects = models.GeoManager()

    @classmethod
    def gtfs_generate(cls, source, reader):
        shape_id = None
        coords = []
        for row in reader:
            if (shape_id is not None) and (shape_id != row['shape_id']):
                path = geos.LineString(coords)
                coords = []
                yield Shape(source=source, shape_id=shape_id, path=path)
            
            shape_id = row['shape_id']
            coords.append((float(row['shape_pt_lon']), float(row['shape_pt_lat'])))
        
        if shape_id is not None:
            path = geos.LineString(coords)
            yield Shape(source=source, shape_id=shape_id, path=path)

    class Meta:
        unique_together = (("source", "shape_id"))

#class Segment(models.Model, GTFSModel):
#    source = models.ForeignKey(settings.GTFS_SOURCE_MODEL, null=True, db_index=True)
#    line_string = models.LineStringField()
#    min_lat = models.FloatField()
#    max_lat = models.FloatField()
#    min_lon = models.FloatField()
#    max_lon = models.FloatField()
#
#    def __eq__(self, other):
#        return other.source == self.source and \
#            other.line_string == self.line_string

#class ShapeSegments(models.Model, GTFSModel):
#    shape = models.ForeignKey('Shape')
#    segment = models.ForeignKey('Segment')
#    reverse = models.BooleanField()
#    position = models.IntegerField()

class Frequency(models.Model, GTFSModel):
    trip = models.ForeignKey('Trip', related_name='frequencies')
    start_time = models.IntegerField(null=True)
    start_time_days = models.IntegerField(null=True)
    end_time = models.IntegerField(null=True)
    end_time_days = models.IntegerField(null=True)
    headway_secs = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Frequencies"

    @classmethod
    def gtfs_populate(cls, o, row):
        o.start_time, o.start_time_days = cls.gtfs_parse_hms_days(row['start_time'])
        o.end_time, o.end_time_days = cls.gtfs_parse_hms_days(row['end_time'])
        return ('start_time', 'end_time')

class Transfer(models.Model, GTFSModel):
    TRANSFER_TYPES = (
        (0, "This is a recommended transfer point between two routes."),
        (1, "This is a timed transfer point between two routes. The departing vehicle is expected to wait for the arriving one, with sufficient time for a passenger to transfer between routes"),
        (2, "This transfer requires a minimum amount of time between arrival and departure to ensure a connection."),
        (3, "Transfers are not possible between routes at this location."),
    )
    from_stop = models.ForeignKey('Stop', related_name='transfers_from')
    to_stop = models.ForeignKey('Stop', related_name='transfers_to')
    transfer_type = models.IntegerField(choices=TRANSFER_TYPES, default=0)
    min_transfer_time = models.IntegerField(null=True)

class UniversalCalendar(models.Model):
    service = models.ForeignKey('Service', related_name='all_dates')
    date = models.DateField(db_index=True)
    
    class Meta:
        unique_together = (("service", "date"),)
    
    def __unicode__(self):
        return unicode(self.date)
    
    @classmethod
    def gtfs_rebuild(cls, source):
        print "%s..." % cls.__name__
        start_time = time.time()

        # delete old records
        cls.objects.filter(service__source=source).delete()

        removes = set()
        for e in CalendarDate.objects.filter(service__source=source).iterator():
            if e.is_added:
                cls.objects.create(service_id=e.service_id, date=e.date)
            else:
                removes.add((e.service_id, e.date))
        
        for c in Calendar.objects.filter(service__source=source).iterator():
            for d in c.get_dates():
                if (c.service_id, d) not in removes:
                    cls.objects.create(service_id=c.service_id, date=d)

        processing_time = time.time() - start_time
        print '  %d records, %.0f seconds' % (cls.objects.filter(service__source=source).count(), processing_time)
