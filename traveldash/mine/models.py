from datetime import timedelta, datetime, date
import urllib2

import lxml.html
from django.db import models
from django.db.models import Q, Min
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from traveldash.gtfs.models import Route, StopTime, Stop, SourceBase


class GTFSSourceManager(models.Manager):
    def need_update(self, updateable=True):
        """
        Return sources needing an update, based on the update_freq/last_update attributes.
        updateable can be True/False/None to return Updateable/Not-updateable/Both.
        """
        qs = self.get_query_set()
        qs = qs.extra(where=("(last_update IS NULL) OR (last_update + CAST(textcat(text(update_freq), text(' days')) as interval) <= NOW())",))
        if updateable is True:
            qs = qs.exclude(zip_url='', page_url='', page_xpath='')
        elif updateable is False:
            qs = qs.filter(zip_url='', page_url='', page_xpath='')
        return qs


class GTFSSource(SourceBase):
    web_url = models.URLField(blank=True, help_text='Website of the source (for linking)')

    zip_url = models.URLField(blank=True, help_text='If a static link to the latest ZIP exists')
    page_url = models.URLField(blank=True, help_text='URL of the page containing the link to the ZIP file')
    page_xpath = models.CharField(max_length=200, blank=True, help_text='XPath to the ZIP URL in the page described by page_url.')

    last_update = models.DateTimeField(null=True, blank=True)
    update_freq = models.IntegerField('Update frequency', default=14, help_text='How often this feed should be updated (days)')

    objects = GTFSSourceManager()

    @property
    def can_autoupdate(self):
        return bool(self.zip_url or (self.page_url and self.page_xpath))

    def download_zip(self, fp):
        """
        Download the ZIP file into the specified file-like object. If there is no way to
        auto-download from this source, raises a ValueError.
        """
        zip_url = self.get_zip_url()
        zip_req = urllib2.urlopen(zip_url)
        for chunk in iter(lambda: zip_req.read(64 * 1024), ''):
            fp.write(chunk)
        fp.flush()

    def get_zip_url(self):
        if self.zip_url:
            return self.zip_url
        elif self.page_url and self.page_xpath:
            page_doc = lxml.html.parse(self.page_url).getroot()
            page_doc.make_links_absolute(self.page_url)
            xpath_result = page_doc.xpath(self.page_xpath)
            if len(xpath_result) != 1:
                raise ValueError("XPath expression didn't resolve to a single result (got %d)" % len(xpath_result))
            elif not len(xpath_result[0]):
                raise ValueError("XPath expression ended up with an empty result")
            else:
                return xpath_result[0]
        else:
            raise ValueError("No ZIP URL found for Source '%s' (%s) - check zip_url/page_url/page_xpath" % (unicode(self), self.pk))


class Dashboard(models.Model):
    user = models.ForeignKey('auth.User', related_name='dashboards')
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

        return sorted(next, key=lambda x: x[2] - timedelta(minutes=x[0].walk_time_start))[:count]

    def as_json(self):
        c = {
            "name": self.name,
            "warning_time": self.warning_time,
            "routes": dict([(route.id, route.as_json()) for route in self.routes.all()]),
        }
        c.update(self.json_update())
        return c

    def json_update(self):
        c = {
            "departures": [],
            "warning_time": self.warning_time,
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
                "walk_time_start": route.walk_time_start,
            })
        return c

    def sources(self):
        return GTFSSource.objects.filter(pk__in=self.routes.values('routes__agency__source__pk').distinct().values_list('routes__agency__source__pk', flat=True))


class DashboardRouteManager(models.Manager):
    def unlink_stops(self):
        for dr in DashboardRoute.objects.all():
            dr.from_stop = None
            dr.to_stop = None
            dr.save()

    def relink_stops(self):
        for dr in DashboardRoute.objects.all():
            dr.from_stop = Stop.objects.get(code=dr.from_stop_code)
            dr.to_stop = Stop.objects.get(code=dr.to_stop_code)
            dr.save()


class DashboardRoute(models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='routes')
    name = models.CharField(max_length=50, blank=True)
    from_stop_code = models.CharField(max_length=20, editable=False)
    from_stop = models.ForeignKey('gtfs.Stop', verbose_name='Which stop do you leave from?', related_name='dashboard_routes_start', null=True)
    to_stop_code = models.CharField(max_length=20, editable=False)
    to_stop = models.ForeignKey('gtfs.Stop', verbose_name='Which stop do you go to?', related_name='dashboard_routes_end', null=True)
    routes = models.ManyToManyField('gtfs.Route')
    walk_time_start = models.PositiveIntegerField('How long to walk there?', default=0, help_text='minutes')
    walk_time_end = models.PositiveIntegerField('How long to walk from there?', default=0, help_text='minutes')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = DashboardRouteManager()

    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def update_stops(cls, sender, instance, **kwargs):
        if instance.from_stop:
            instance.from_stop_code = instance.from_stop.code

        if instance.to_stop:
            instance.to_stop_code = instance.to_stop.code

    @classmethod
    def update_routes(cls, sender, instance, **kwargs):
        if instance.from_stop and instance.to_stop:
            instance.routes = Route.objects.between_stops(instance.from_stop, instance.to_stop)
        else:
            instance.routes.clear()

    def next(self, start_time=None, count=10):
        """ Get the next Trips departing for this route """
        if start_time is None:
            start_time = datetime.now()

        today = start_time.date()
        tomorrow = today + timedelta(days=1)
        dt = start_time.time()
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

pre_save.connect(DashboardRoute.update_stops, sender=DashboardRoute)
post_save.connect(DashboardRoute.update_routes, sender=DashboardRoute)
