import os
from functools import lru_cache
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models import Sum, IntegerField, Case, Value, When, F
from django.conf import settings
from djgeojson.fields import PointField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from django_extensions.db.fields import AutoSlugField
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices



def desde_hasta(qs):
    qs = qs.values_list('numero', flat=True).order_by('numero')
    inicio, fin = qs.first(), qs.last()
    if inicio == fin:
        return inicio
    return f'{inicio} - {fin}'


class Seccion(models.Model):
    numero = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Sección electoral'
        verbose_name_plural = 'Secciones electorales'

    def __str__(self):
        return f"{self.numero} - {self.nombre}"


class Circuito(models.Model):
    seccion = models.ForeignKey(Seccion)
    numero = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Circuito electoral'
        verbose_name_plural = 'Circuitos electorales'
        ordering = ('numero',)

    def __str__(self):
        return f"{self.numero} - {self.nombre}"


class LugarVotacion(models.Model):
    circuito = models.ForeignKey(Circuito)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    calidad = models.CharField(max_length=20, help_text='calidad de la geolocalizacion', editable=False, blank=True)
    electores = models.PositiveIntegerField(null=True, blank=True)
    geom = PointField(null=True)

    # denormalizacion para hacer queries más simples
    latitud = models.FloatField(null=True, editable=False)
    longitud = models.FloatField(null=True, editable=False)

    class Meta:
        verbose_name = 'Lugar de votación'
        verbose_name_plural = "Lugares de votación"


    def save(self, *args, **kwargs):
        if self.geom:
            self.longitud, self.latitud = self.geom['coordinates']
        else:
            self.longitud, self.latitud = None, None
        super().save(*args, **kwargs)

    @property
    def coordenadas(self):
        return f'{self.latitud},{self.longitud}'

    @property
    def direccion_completa(self):
        return f'{self.direccion} {self.barrio} {self.ciudad}'

    @property
    def mesas_desde_hasta(self):
        return desde_hasta(self.mesas)

    @property
    def color(self):
        if self.mesa_testigo:
            return 'blue'
        if not self.asignacion.exists():
            return 'red'
        elif self.asignacion.filter(ingreso__isnull=False).exists():
            return 'green'
        return 'orange'

    @property
    def seccion(self):
        return str(self.circuito.seccion)

    def __str__(self):
        return f"{self.nombre} - {self.circuito}"


def path_documento(instance, filename):
    # file will be uploaded to MEDIA_ROOT/
    _, ext = os.path.splitext(filename)
    path = f'{instance.circuito.seccion.numero}/{instance.circuito.numero}/{instance.tipo}'
    return f'{path}/{instance.mesa.numero}.{ext}'


path_foto_acta = path_documento    # compatibilidad


class Documento(models.Model):
    TIPO = Choices(('acta_oficial', 'Acta oficial'),
                   ('acta_partidaria', 'Acta Partidaria'),
                   ('telegrama_oficial', 'Telegrama oficial'))
    tipo = models.CharField(max_length=50, choices=TIPO)
    archivo = models.ImageField(upload_to=path_documento, null=True, blank=True)
    subido_por = models.ForeignKey('auth.User', null=True, blank=True, editable=False)
    mesa = models.ForeignKey('Mesa')


class Mesa(models.Model):
    categorias = models.ManyToManyField('Categoria', help_text='Qué se vota en esta mesa')
    circuito = models.ForeignKey('Circuito')
    lugar_votacion = models.ForeignKey(
        LugarVotacion, verbose_name='Lugar de votacion',
        null=True, related_name='mesas'
    )
    numero = models.PositiveIntegerField()
    es_testigo = models.BooleanField(default=False)

    electores = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return f"Mesa {self.numero}"


class Opcion(models.Model):
    orden = models.PositiveIntegerField(help_text='Orden en el acta')
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=10, blank=True)

    orden = models.PositiveIntegerField(
        help_text='Orden en la boleta', null=True, blank=True)

    es_partido = models.BooleanField(default=True)
    obligatorio = models.BooleanField(default=True,
        help_text='Si se deshabilita, la carga de votos para esta opción no será obligatoria')
    color = models.CharField(max_length=20, blank=True)
    codigo_dne = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Eleccion(models.Model):
    nombre = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=['nombre'])
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Elección'
        verbose_name_plural = 'Elecciones'

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=True,
        help_text='Nombre descriptivo interno. Ej: Elecciones de Concejales de Tres de Febrero')
    eleccion = models.ForeignKey('Eleccion', related_name='categorias')
    cargo = models.CharField(max_length=50,
        help_text='Nombre del cargo/s elegible. Ej. Senadores Nacionales')
    slug = AutoSlugField(populate_from=['cargo'])
    orden = models.PositiveIntegerField(
        help_text='Orden en la boleta', null=True, blank=True)
    opciones = models.ManyToManyField('Opcion')

    class Meta:
        verbose_name = 'Categoría elegible'
        verbose_name_plural = 'Categorías elegibles'

    def __str__(self):
        return f'{self.eleccion} - {self.nombre}'

    @property
    @lru_cache(128)
    def agregaciones(self):
        opciones = {}
        for id in self.opciones.order_by('orden').values_list('id', flat=True):
            opciones[str(id)] = Sum(
                Case(
                    When(
                        opcion__id=id,
                        categoria__id=self.id,
                        then=F('votos')
                    ),
                output_field=IntegerField()
                )
            )
        return opciones
