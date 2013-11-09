import datetime
import factory
from factory.django import DjangoModelFactory

from core.models import Opcion


class EleccionFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.Eleccion'
    nombre = factory.Sequence(lambda n: "Elecciones - %d" % n)
    fecha = datetime.date(2013, 10, 27)

    @factory.post_generation
    def opciones(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of opciones were passed in, use them
            for opcion in extracted:
                OpcionFactory(eleccion=self, nombre=opcion)


class ProvinciaFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.Provincia'
    dne_id = factory.Sequence(lambda n: n)
    nombre = factory.Sequence(lambda n: 'provincia %d' % n)


class MunicipioFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.Municipio'
    dne_id = factory.Sequence(lambda n: n)
    nombre = factory.Sequence(lambda n: 'muni %d' % n)
    provincia = factory.SubFactory(ProvinciaFactory)


class CircuitoFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.Circuito'
    municipio = factory.SubFactory(MunicipioFactory)
    numero = factory.Sequence(lambda n: '%02d' % n)


class OpcionFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.Opcion'
    eleccion = factory.SubFactory(EleccionFactory)
    nombre = factory.Sequence(lambda n: 'Opcion %d' % n)


class MesaFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.Mesa'
    circuito = factory.SubFactory(CircuitoFactory)
    numero = factory.Sequence(lambda n: n)

    @factory.post_generation
    def resultado(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of opciones were passed in, use them
            for opcion_nombre, votos in extracted:
                opcion = Opcion.objects.get(nombre=opcion_nombre)
                VotoMesaOficialFactory(mesa=self, opcion=opcion, votos=votos)


class VotoMesaOficialFactory(DjangoModelFactory):
    FACTORY_FOR = 'core.VotoMesaOficial'
    mesa = factory.SubFactory(MesaFactory)
    opcion = factory.SubFactory(Opcion)
