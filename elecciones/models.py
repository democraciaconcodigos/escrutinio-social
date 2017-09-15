import os
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


def path_foto_acta(instance, filename):
    # file will be uploaded to MEDIA_ROOT/
    _, ext = os.path.splitext(filename)
    return f'actas/{instance.circuito.seccion.numero}/{instance.circuito.numero}/{instance.numero}{ext}'


class Mesa(models.Model):
    eleccion = models.ForeignKey('Eleccion')
    circuito = models.ForeignKey('Circuito')
    lugar_votacion = models.ForeignKey(
        LugarVotacion, verbose_name='Lugar de votacion',
        null=True, related_name='mesas'
    )
    numero = models.PositiveIntegerField()
    es_testigo = models.BooleanField(default=False)

    foto_acta = models.ImageField(upload_to=path_foto_acta, null=True, blank=True)
    foto_acta = models.ImageField(upload_to=path_foto_acta, null=True, blank=True)
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
    color = models.CharField(max_length=20, blank=True)
    codigo_dne = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Eleccion(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    fecha = models.DateTimeField(blank=True, null=True)
    opciones = models.ManyToManyField(Opcion)

    @classmethod
    def opciones_actuales(cls):
        if cls.objects.last():
            return cls.objects.last().opciones.all()
        return Opcion.objects.none()

    class Meta:
        verbose_name = 'Elección'
        verbose_name_plural = 'Elecciones'

    def __str__(self):
        return self.nombre

