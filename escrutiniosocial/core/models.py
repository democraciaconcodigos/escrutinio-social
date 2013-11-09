from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Provincia(models.Model):
    dne_id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Municipio(models.Model):
    dne_id = models.PositiveIntegerField(primary_key=True)
    provincia = models.ForeignKey(Provincia)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Circuito(models.Model):
    municipio = models.ForeignKey('Municipio')
    numero = models.CharField(max_length=100)

    def __unicode__(self):
        return u"Circuito %s (%s)" % (self.numero, self.municipio)


class LugarVotacion(models.Model):
    dne_id = models.PositiveIntegerField(primary_key=True)
    circuito = models.ForeignKey('Circuito')
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)


class Mesa(models.Model):
    circuito = models.ForeignKey('Circuito')
    lugarvotacion = models.ForeignKey('LugarVotacion', null=True)
    numero = models.IntegerField(max_length=100)
    url = models.URLField(null=True)

    @property
    def computados(self):
        return self.votomesa_set.aggregate(Sum('votos'))['votos__sum']

    def __unicode__(self):
        return u"Mesa %s (%s)" % (self.numero, self.circuito)


class Eleccion(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateTimeField()

    def __unicode__(self):
        return "%s - %s" % (self.nombre, self.fecha.strftime('%d/%m/%Y'))


class Opcion(models.Model):
    # partido, blanco, etc.
    eleccion = models.ForeignKey(Eleccion, related_name='opciones')
    nombre = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.nombre


class AbstractVotoMesa(models.Model):
    mesa = models.ForeignKey('Mesa')
    opcion = models.ForeignKey('Opcion')
    votos = models.IntegerField()

    class Meta:
        abstract = True
        unique_together = ('mesa', 'opcion')

    def __unicode__(self):
        return u"%s: %d" % (self.opcion, self.votos)


class VotoMesaOficial(AbstractVotoMesa):
    pass


class VotoMesaSocial(AbstractVotoMesa):
    usuario = models.ForeignKey(User)


class VotoMesaOCR(AbstractVotoMesa):
    pass


