# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from fancy_cache import cache_page
from rest_framework import routers, serializers

from rest_framework_jwt.views import obtain_jwt_token

cached = cache_page(3600 * 24 * 7)

router = routers.DefaultRouter()
router.register('mesa', views.MesaViewSet)
router.register('mesaDocumento', views.MesaDocumentoViewSet)

urlpatterns = [

    # url('^escuelas.geojson$', cached(views.LugaresVotacionGeoJSON.as_view()), name='geojson'),
    # url('^escuelas/(?P<pk>\d+)$', views.EscuelaDetailView.as_view(), name='detalle_escuela'),
    # url('^mapa/$', cached(views.Mapa.as_view()), name='mapa'),

    # # url('^mapa/(?P<elecciones_slug>\w+)/$', cached(views.MapaResultadosOficiales.as_view()), name='mapa-resultados'),
    # url('^mapa/(?P<elecciones_slug>\w+)/(?P<pk>\d+)$', views.ResultadoEscuelaDetailView.as_view()),
    # url('^mapa/(?P<elecciones_slug>\w+)/resultados.geojson$', cached(views.ResultadosOficialesGeoJSON.as_view()), name='resultados-geojson'),

    url('^resultados/', cached(views.Resultados.as_view()), name='resultados'),
    url(r'^login', obtain_jwt_token),
]

urlpatterns += router.urls
