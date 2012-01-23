from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from traveldash import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('traveldash.mine.urls')),

    url(r'', include('social_auth.urls')),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
