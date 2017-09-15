# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url('^inicio$', views.Inicio.as_view(), name='inicio'),
    url('^mis-datos$', views.MisDatos.as_view(), name='mis-datos'),
    url('^cargar/(?P<asignacion_id>\d+)$', views.cargar_resultados, name='cargar'),
    url('^mis-datos/profile$', views.MisDatosUpdate.as_view(), name='mis-datos-update'),
    url('^mis-datos/password$', views.CambiarPassword.as_view(), name='cambiar-password'),
]
