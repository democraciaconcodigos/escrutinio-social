from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api.v1 import *

# FIXME: Debe haber una forma mejor de hacer esto...
v1_api = Api(api_name='v1')
v1_api.register(ProvinciaResource())
v1_api.register(MunicipioResource())
v1_api.register(CircuitoResource())
v1_api.register(LugarVotacionResource())
v1_api.register(MesaResource())
v1_api.register(OpcionResource())
v1_api.register(EleccionResource())
v1_api.register(VotoMesaOficialResource())
v1_api.register(VotoMesaSocialResource())
v1_api.register(VotoMesaOCRResource())

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    (r'^api/', include(v1_api.urls))
)
