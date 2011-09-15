from django.conf.urls.defaults import *

from traveldash.mine.views import DashboardDelete

urlpatterns = patterns('traveldash.mine.views',
    url(r'^$', 'home'),
    url(r'^login/$', 'login'),

    url(r'^mine/$', 'dashboard_list'),
    url(r'^new/$', 'dashboard_create'),

    url(r'^(?P<pk>\d+)/$', 'dashboard'),
    url(r'^(?P<pk>\d+)/data/$', 'dashboard_update'),
    url(r'^(?P<pk>\d+)/edit/$', 'dashboard_edit'),
    url(r'^(?P<pk>\d+)/delete/$', DashboardDelete.as_view(), name="dashboard-delete"),
)