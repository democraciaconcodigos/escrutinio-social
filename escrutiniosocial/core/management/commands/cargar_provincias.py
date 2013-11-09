# -*- coding: utf-8 -*-

import csv

from django.core.management.base import BaseCommand, CommandError

from core.models import Municipio, Provincia


class Command(BaseCommand):
    """Importa provincias y departamentos desde archivo CSV."""
    args = '<csv_file>'
    help = 'Importa informacion de provincias y departamentos'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Missing csv file parameter')

        with open(args[0]) as csv_file:
            # csv_file is utf-8 encoded
            data = csv.DictReader(csv_file)
            for entry in data:
                provincia, _ = Provincia.objects.get_or_create(
                    dne_id=entry['codigo_provincia'],
                    nombre=entry['provincia'].decode('utf-8'))

                municipio, created = Municipio.objects.get_or_create(
                    dne_id=entry['codigo_departamento'],
                    nombre=entry['departamento'].decode('utf-8'),
                    provincia=provincia)

                if created:
                    self.stdout.write(
                        u'Agregado "%s/%s"' % (provincia.nombre,
                                               municipio.nombre))
