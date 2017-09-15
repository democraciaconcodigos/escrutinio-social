Escrutinio Social
=================

Una plataforma web para un recuento provisorio de resultados electorales basado en la colaboración de voluntari@s.

Es una inciativa de `Open Data Córdoba <https://github.com/OpenDataCordoba>`_ junto a diversas organizaciones
sociales y políticas, con el fin de incrementar la transparencia y fortalecer nuestra democracia.


Entorno de desarrollo
---------------------

Es un proyecto basado en Django. Requiere Python 3.6 y Postgresql.


Podés ver este `tutorial <https://tutorial.djangogirls.org/es/django_installation/>`_
para instrucciones detalladas.

1. Crear un virtualenv
2. ``pip install -r requirements.txt``
3. crear base de datos postgres y configurar los datos en ``escrutiniosocial/local_settings.py``

4. ``python manage.py migrate``
5. cargar fixtures ``python manage.py loaddata fixtures/*``
6. ``python manage.py runserver``

Un superusuario ``admin`` con clave ``admin`` se habrá cargado











