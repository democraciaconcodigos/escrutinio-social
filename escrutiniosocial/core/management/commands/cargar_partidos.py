# -*- coding: utf-8 -*-

import csv

from django.core.management.base import BaseCommand, CommandError

from core.models import Opcion


class Command(BaseCommand):
    """Importa partidos desde archivo CSV."""
    args = '<csv_file>'
    help = 'Importa informacion de partidos'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Missing csv file parameter')

        with open(args[0]) as csv_file:
            # csv_file is utf-8 encoded
            data = csv.DictReader(csv_file)
            for entry in data:
                opcion, created = Opcion.objects.get_or_create(
                    dne_id=entry['codigo_partido'],
                    nombre=entry['partido'].decode('utf-8'))
                if created:
                    self.stdout.write(u'Agregado "%s"' % opcion.nombre)
