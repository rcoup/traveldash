from datetime import datetime, timedelta

from django.contrib.gis import admin

from traveldash.mine.models import Dashboard, DashboardRoute, GTFSSource, City, Alert


def get_admin_metrics():
    from django.contrib.auth.models import User
    from traveldash.gtfs.models import UniversalCalendar, Route, Stop

    last_week = datetime.now() - timedelta(days=7)
    metrics = (
        ('Number of Dashboards', Dashboard.objects.count()),
        ('Number of Dashboard Routes', DashboardRoute.objects.count()),
        ('Number of Users', User.objects.count()),
        ('Last week - Dashboards created', Dashboard.objects.filter(created_at__gte=last_week).count()),
        ('Last week - Dashboards viewed', Dashboard.objects.filter(last_viewed__gte=last_week).count()),
        ('Last week - new Users', User.objects.filter(date_joined__gte=last_week).count()),
        ('Last week - scheduled Services', UniversalCalendar.objects.filter(date__gte=last_week.date()).count()),
        ('Last week - Source updates', GTFSSource.objects.filter(last_update__gte=last_week).count()),
        ('Number of service Routes', Route.objects.count()),
        ('Number of service Stops', Stop.objects.count()),
        ('Errors - empty Dashboards', Dashboard.objects.filter(routes__isnull=True).count()),
        ('Errors - unlinked Dashboard Route stops', DashboardRoute.objects.unlinked_stops().count()),
        ('Errors - Dashboard Routes with no Services', DashboardRoute.objects.no_routes().count()),
    )
    return metrics


class DashboardRouteInline(admin.StackedInline):
    model = DashboardRoute
    raw_id_fields = ('from_stop', 'to_stop',)
    readonly_fields = ('routes', 'next')
    extra = 1

    def next(self, obj):
        now = datetime.now()
        msg = []
        for trip, departing, service_date in obj.next(now, count=5):
            td = departing - now
            h = "%dh " % (td.seconds / 3600) if (td.seconds > 3600) else ""
            m = "%dm" % (td.seconds % 3600 / 60)
            msg.append(u"%s in %s%s" % (trip.route.short_name, h, m))

        return u"; ".join(msg)


class DashboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'name', 'created_at', 'last_viewed')
    list_display_links = ('id', 'name',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'name',)
    list_filter = ('created_at', 'city', 'last_viewed')
    raw_id_fields = ('user',)
    readonly_fields = ('next',)
    inlines = (
        DashboardRouteInline,
    )

    def next(self, obj):
        now = datetime.now()
        msg = []
        for route, trip, dep, arr in obj.next(now, count=5):
            td = dep - now
            h = "%dh " % (td.seconds / 3600) if (td.seconds > 3600) else ""
            m = "%dm" % (td.seconds % 3600 / 60)
            msg.append(u"%s %s in %s%s" % (route, trip.route.short_name, h, m))

        return u"; ".join(msg)


class GTFSSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'get_can_autoupdate', 'last_update', 'update_freq',)

    def get_can_autoupdate(self, obj):
        return obj.can_autoupdate
    get_can_autoupdate.boolean = True
    get_can_autoupdate.short_description = 'Auto-update?'


class CityAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'country')


class AlertAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'city', 'get_is_valid', 'valid_from', 'valid_to')

    def get_is_valid(self, obj):
        return obj.is_valid
    get_is_valid.boolean = True
    get_is_valid.short_description = 'Valid?'


admin.site.register(City, CityAdmin)
admin.site.register(GTFSSource, GTFSSourceAdmin)
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Alert, AlertAdmin)
