from datetime import datetime

from django.contrib import admin

from traveldash.mine.models import Dashboard, DashboardRoute, GTFSSource


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
    list_display = ('user', 'name', 'created_at',)
    list_display_links = ('name',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'name',)
    list_filter = ('created_at',)
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
    pass

admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(GTFSSource, GTFSSourceAdmin)
