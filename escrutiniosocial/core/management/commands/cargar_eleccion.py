# -*- coding: utf-8 -*-

import csv
import os

from django.core.management.base import BaseCommand, CommandError

from core.models import (
    Circuito,
    Eleccion,
    Mesa,
    Municipio,
    Opcion,
    Provincia,
    VotoMesaOficial,
)


class Command(BaseCommand):
    """Importa resultados de elección desde archivo CSV."""
    args = '<eleccion_name> <csv_file>'
    help = 'Importa informacion de resultados'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Missing required parameter(s)')

        eleccion = Eleccion.objects.create(nombre=args[0])

        with open(args[1]) as csv_file:
            data = csv.DictReader(csv_file)

            provincia = None
            municipio = None
            circuito = None
            for entry in data:
                if (provincia is None or
                        provincia.dne_id != entry['codigo_provincia']):
                    provincia = Provincia.objects.get(
                        dne_id=entry['codigo_provincia'])
                    municipio = None

                if (municipio is None or
                        municipio.dne_id != entry['codigo_departamento']):
                    municipio = Municipio.objects.get(
                        dne_id=entry['codigo_departamento'],
                        provincia=provincia)
                    circuito = None

                if (circuito is None or
                        circuito.numero != entry['codigo_circuito']):
                    circuito, _ = Circuito.objects.get_or_create(
                        municipio=municipio, numero=entry['codigo_circuito'])

                mesa, _ = Mesa.objects.get_or_create(
                    circuito=circuito, numero=entry['codigo_mesa'])

                # agregar log de voto oficial
                dne_id = entry['codigo_votos']
                opcion = Opcion.objects.get(dne_id=dne_id)
                eleccion.opciones.add(opcion)
                votos, _ = VotoMesaOficial.objects.get_or_create(
                    eleccion=eleccion, mesa=mesa, opcion=opcion,
                    votos=int(entry['votos']))

                self.stdout.write('.', ending='')
                self.stdout.flush()
