from django.conf.urls import patterns, include, url

from django.contrib import admin
import api.urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    (r'^api/', include(api.urls)),
)
