from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView
from django.conf import settings

from traveldash import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('traveldash.mine.urls')),

    url(r'^login/$', TemplateView.as_view(template_name="login.html")),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'', include('social_auth.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # these are normally handled by apache
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^favicon.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
        url(r'^robots.txt$', RedirectView.as_view(url='/static/robots.txt')),
    )
