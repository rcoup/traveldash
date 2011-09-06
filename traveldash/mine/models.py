from datetime import timedelta, datetime, date

from django.db import models
from django.db.models import Q, Min

from traveldash.gtfs.models import Route, Trip, StopTime

class Dashboard(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    warning_time = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name)

    def next(self, start_time=None, count=10):
        if start_time is None:
            start_time = datetime.now()

        next = []
        for route in self.routes.all():
            for trip, dep, arr in route.next_with_arrivals(start_time, count):
                next.append((route, trip, dep, arr))
        
        return sorted(next, key=lambda x: x[2]-timedelta(seconds=x[0].walk_time_start))[:count]

class DashboardRoute(models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='routes')
    name = models.CharField(max_length=50)
    from_stop = models.ForeignKey('gtfs.Stop', related_name='dashboard_routes_start')
    to_stop = models.ForeignKey('gtfs.Stop', related_name='dashboard_routes_end')
    routes = models.ManyToManyField('gtfs.Route')
    walk_time_start = models.IntegerField(default=0, help_text='Walk time at the start of the route (secs)')
    walk_time_end = models.IntegerField(default=0, help_text='Walk time at the end of the route (secs)')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.from_stop and self.to_stop:
            self.routes = Route.objects.between_stops(self.from_stop, self.to_stop)
        return super(DashboardRoute, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.name)

    def next(self, start_time=None, count=10):
        """ Get the next Trips departing for this route """
        if start_time is None:
            start_time = datetime.now()

        departure = start_time + timedelta(seconds=self.walk_time_start)
        
        today = departure.date()
        tomorrow = today + timedelta(days=1)
        dt = departure.time()
        dt_int = dt.hour * 3600 + dt.minute * 60 + dt.second
        
        qs = StopTime.objects.filter(trip__route__in=self.routes.all(), stop=self.from_stop, pickup_type=StopTime.PICKUP)
        qs = qs.filter(Q(trip__service__all_dates__date=today, departure_time__gte=dt_int)
                       | Q(trip__service__all_dates__date=tomorrow))
        qs = qs.select_related('trip').annotate(service_date=Min('trip__service__all_dates__date'))
        qs = qs.order_by('trip__service__all_dates__date', 'departure_days', 'departure_time')[:count]

        for stop_time in qs:
            yield (stop_time.trip, stop_time.departing(stop_time.service_date), stop_time.service_date)
    
    def next_with_arrivals(self, start_time=None, count=10):
        if start_time is None:
            start_time = datetime.now()

        for trip, departing, service_date in self.next(start_time, count):
            arr_st = trip.stop_times.filter(stop=self.to_stop, drop_off_type=StopTime.DROPOFF)[0]
            arr = arr_st.arriving(service_date)
            yield (trip, departing, arr)
