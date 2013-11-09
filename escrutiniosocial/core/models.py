from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Provincia(models.Model):
    dne_id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Municipio(models.Model):
    dne_id = models.PositiveIntegerField()
    provincia = models.ForeignKey(Provincia)
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ('dne_id', 'provincia')

    def __unicode__(self):
        return self.nombre


class Circuito(models.Model):
    municipio = models.ForeignKey(Municipio)
    numero = models.CharField(max_length=100)

    def __unicode__(self):
        return u"Circuito %s (%s)" % (self.numero, self.municipio)


class LugarVotacion(models.Model):
    dne_id = models.PositiveIntegerField(primary_key=True)
    circuito = models.ForeignKey(Circuito)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)


class Mesa(models.Model):
    circuito = models.ForeignKey(Circuito)
    lugarvotacion = models.ForeignKey(LugarVotacion, null=True)
    numero = models.IntegerField(max_length=100)
    url = models.URLField(null=True)

    @property
    def computados(self):
        return self.votomesa_set.aggregate(Sum('votos'))['votos__sum']

    def __unicode__(self):
        return u"Mesa %s (%s)" % (self.numero, self.circuito)


class Opcion(models.Model):
    dne_id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Eleccion(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateTimeField(blank=True, null=True)
    opciones = models.ManyToManyField(Opcion)

    def __unicode__(self):
        return self.nombre


class AbstractVotoMesa(models.Model):
    eleccion = models.ForeignKey(Eleccion)
    mesa = models.ForeignKey(Mesa)
    opcion = models.ForeignKey(Opcion)
    votos = models.IntegerField()

    class Meta:
        abstract = True
        unique_together = ('eleccion', 'mesa', 'opcion')

    def __unicode__(self):
        return u"%s - %s: %d" % (self.eleccion, self.opcion, self.votos)


class VotoMesaOficial(AbstractVotoMesa):
    pass


class VotoMesaSocial(AbstractVotoMesa):
    usuario = models.ForeignKey(User)


class VotoMesaOCR(AbstractVotoMesa):
    pass
