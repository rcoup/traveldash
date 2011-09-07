from django.conf.urls.defaults import *

from traveldash.mine.views import dashboard

urlpatterns = patterns('',
    url(r'^(?P<dashboard_slug>\w+)/$', dashboard, name="dashboard"),
)