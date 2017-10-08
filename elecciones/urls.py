# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from fancy_cache import cache_page

cached = cache_page(3600 * 24 * 7)

urlpatterns = [
    url('(?P<slug>[-\w]+)/$', cached(views.Resultados.as_view()), name='resultados'),
]
