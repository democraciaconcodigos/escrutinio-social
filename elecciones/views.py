import json
from urllib import parse
from functools import lru_cache
from collections import OrderedDict
from django.http import HttpResponse, Http404
from django.utils.text import get_text_list
from .models import *
from django.db.models import Q, F, Sum
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from djgeojson.views import GeoJSONLayerView
from .models import LugarVotacion, Circuito
from fiscales.models import  Voluntario, VotoMesaOficial, VotoMesaReportado
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class StaffOnlyMixing:

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Resultados(StaffOnlyMixing, TemplateView):
    template_name = "elecciones/resultados.html"

    def dispatch(self, *args, **kwargs):
        self.eleccion = get_object_or_404(Eleccion, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    @property
    @lru_cache(128)
    def filtros(self):
        """
        a partir de los argumentos de urls, devuelve
        listas de seccion / circuito etc. para filtrar
        """
        if 'mesa' in self.request.GET:
            return Mesa.objects.filter(id__in=self.request.GET.getlist('mesa'))
        elif 'lugarvotacion' in self.request.GET:
            return LugarVotacion.objects.filter(id__in=self.request.GET.getlist('lugarvotacion'))
        elif 'circuito' in self.request.GET:
            return Circuito.objects.filter(id__in=self.request.GET.getlist('circuito'))
        elif 'seccion' in self.request.GET:
            return Seccion.objects.filter(id__in=self.request.GET.getlist('seccion'))

    @property
    @lru_cache(128)
    def electores(self):
        lookups = Q()
        meta = {}
        for categoria in self.eleccion.categorias.all():
            if self.filtros:
                if 'mesa' in self.request.GET:
                    lookups = Q(
                        mesas__id__in=self.filtros,
                        mesas__categorias=categoria
                    )
                elif 'lugarvotacion' in self.request.GET:
                    lookups = Q(id__in=self.filtros)
                elif 'circuito' in self.request.GET:
                    lookups = Q(circuito__in=self.filtros)
                elif 'seccion' in self.request.GET:
                    lookups = Q(circuito__seccion__in=self.filtros)

            escuelas = LugarVotacion.objects.filter(lookups).distinct()
            electores = escuelas.aggregate(v=Sum('electores'))['v']
            if electores and 'mesa' in self.request.GET:
                # promediamos los electores por mesa
                mesas_en_escuelas = Mesa.objects.filter(
                    lugar_votacion__in=escuelas,
                    categoria=categoria
                ).count()
                electores = (
                    electores * self.filtros.count() // mesas_en_escuelas
                )
            meta[categoria] = electores or 0
        return meta

    def resultados(self):

        lookups = Q()
        resultados = OrderedDict()

        for categoria in self.eleccion.categorias.order_by('orden'):

            if self.filtros:

                if 'mesa' in self.request.GET:
                    lookups = Q(mesa__in=self.filtros)

                elif 'lugarvotacion' in self.request.GET:
                    lookups = Q(mesa__lugar_votacion__in=self.filtros)

                elif 'circuito' in self.request.GET:
                    lookups = Q(mesa__circuito__in=self.filtros)

                elif 'seccion' in self.request.GET:
                    lookups = Q(mesa__circuito__seccion__in=self.filtros)


            electores = self.electores[categoria]
            # primero para partidos
            result = VotoMesaReportado.objects.filter(
                Q(categoria=categoria) & lookups
            ).aggregate(
                **categoria.agregaciones
            )
            # obtener la instancia de opcion para aquellas
            # opciones que obtuvieron votos
            result = OrderedDict((Opcion.objects.get(id=k), v) for k, v in result.items() if v is not None)

            # total de votos positivos
            positivos = sum(v for k, v in result.items() if k.es_partido)

            # total de votantes
            total = sum(v for k, v in result.items() if k.nombre.lower() == 'total de votos')

            # agregar porcentaje
            result = {k: (v, f'{v*100/total:.2f}') for k, v in result.items()}
            resultados[categoria] = {
                'tabla': result,
                'electores': electores,
                'positivos': positivos,
                'escrutados': total,
                'participacion': f'{total*100/electores:.2f}' if electores else '-'
            }
        return resultados


    def menu_activo(self):
        if not self.filtros:
            return []
        elif isinstance(self.filtros[0], Seccion):
            return (self.filtros[0], None)
        elif isinstance(self.filtros[0], Circuito):
            return (self.filtros[0].seccion, self.filtros[0])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filtros:
            context['para'] = get_text_list(list(self.filtros), " y ")
        else:
            context['para'] = 'Buenos Aires'
        context['eleccion'] = self.eleccion
        context['secciones'] = Seccion.objects.all()
        context['resultados'] = self.resultados()
        context['menu_activo'] = self.menu_activo()
        return context

