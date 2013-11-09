from django.test import TestCase

from core.models import Opcion
from core.factories import EleccionFactory, MesaFactory


OPCIONES = ['blanco', 'nulo', 'ucr', 'fpv']


class TestComputados(TestCase):

    def setUp(self):
        self.eleccion = EleccionFactory(opciones=OPCIONES)

    def test_computados_mesa(self):
        votacion = [5, 1, 10, 20]
        mesa = MesaFactory(resultado=zip(OPCIONES, votacion))
        self.assertEqual(sum(votacion), mesa.computados)

    def test_computados_mesa_independiente_de_otra(self):

        votacion1 = [5, 1, 10, 20]
        mesa1 = MesaFactory(resultado=zip(OPCIONES, votacion1))

        votacion2 = [1, 1, 0, 1]
        mesa2 = MesaFactory(resultado=zip(OPCIONES, votacion2))

        self.assertEqual(sum(votacion1), mesa1.computados)
        self.assertEqual(sum(votacion2), mesa2.computados)
