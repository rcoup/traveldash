from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.conf import settings

from traveldash import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('traveldash.mine.urls')),

    url(r'^login/$', direct_to_template, {'template': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'', include('social_auth.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # these are normally handled by apache
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^favicon.ico$', redirect_to, {'url': '/static/img/favicon.ico'}),
        url(r'^robots.txt$', redirect_to, {'url': '/static/robots.txt'}),
    )
