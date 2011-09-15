from datetime import timedelta, datetime, date

from django.db import models
from django.db.models import Q, Min
from django.db.models.signals import post_save
from django.dispatch import receiver

from traveldash.gtfs.models import Route, Trip, StopTime

class Dashboard(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField("Name of your dashboard?", max_length=50)
    warning_time = models.PositiveIntegerField("How much warning do you need?", default=10, help_text="Minutes to alert before departure")
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('traveldash.mine.views.dashboard', [str(self.pk)])

    @models.permalink
    def get_edit_url(self):
        return ('traveldash.mine.views.dashboard_edit', [str(self.pk)])

    def next(self, start_time=None, count=10):
        if start_time is None:
            start_time = datetime.now()

        next = []
        for route in self.routes.all():
            for trip, dep, arr in route.next_with_arrivals(start_time, count):
                next.append((route, trip, dep, arr))
        
        return sorted(next, key=lambda x: x[2]-timedelta(minutes=x[0].walk_time_start))[:count]

    def as_json(self):
        c = {
            "name": self.name,
            "warning_time": self.warning_time*60,
            "routes": dict([(route.id, route.as_json()) for route in self.routes.all()]),
        }
        c.update(self.json_update())
        return c
    
    def json_update(self):
        c = {
            "departures": [],
        }
        for route, trip, dep, arr in self.next():
            c["departures"].append({
                "route": route.id,
                "trip": {
                    "id": trip.id,
                    "short_name": trip.route.short_name,
                    "long_name": trip.route.long_name,
                    "color": trip.route.color,
                    "text_color": trip.route.text_color,
                    "mode": trip.route.route_type,
                    "mode_label": trip.route.get_route_type_display(),
                },
                "departs": dep.isoformat(),
                "arrives": arr.isoformat(),
            })
        return c

class DashboardRoute(models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='routes')
    name = models.CharField(max_length=50, blank=True)
    from_stop = models.ForeignKey('gtfs.Stop', verbose_name='Which stop do you leave from?', related_name='dashboard_routes_start')
    to_stop = models.ForeignKey('gtfs.Stop', verbose_name='Which stop do you go to?', related_name='dashboard_routes_end')
    routes = models.ManyToManyField('gtfs.Route')
    walk_time_start = models.PositiveIntegerField('How long to walk there?', default=0, help_text='minutes')
    walk_time_end = models.PositiveIntegerField('How long to walk from there?', default=0, help_text='minutes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def update_routes(cls, sender, instance, **kwargs):
        instance.routes = Route.objects.between_stops(instance.from_stop, instance.to_stop)

    def next(self, start_time=None, count=10):
        """ Get the next Trips departing for this route """
        if start_time is None:
            start_time = datetime.now()

        departure = start_time + timedelta(minutes=self.walk_time_start)
        
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

    def as_json(self):
        c = {
            "name": self.name,
            "from": {
                "id": self.from_stop.id,
                "name": self.from_stop.name,
                "walk_time": self.walk_time_start,
            },
            "to": {
                "id": self.to_stop.id,
                "name": self.to_stop.name,
                "walk_time": self.walk_time_end,
            },
        }
        return c

post_save.connect(DashboardRoute.update_routes, sender=DashboardRoute)

