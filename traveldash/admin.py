from django.contrib import admin as _
from django.contrib.admin import *
from django.views.decorators.cache import never_cache


class TravelDashAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        from traveldash.mine.admin import get_admin_metrics

        extra_context = {
            'metrics': get_admin_metrics(),
        }
        return super(TravelDashAdminSite, self).index(request, extra_context=extra_context)

# make admin.autodiscover() still work...
site = TravelDashAdminSite()
_.site = site
