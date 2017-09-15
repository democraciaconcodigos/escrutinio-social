Escrutinio ciudadano
====================

Una plataforma para un recuento provisorio paralelo basado en la colaboracion de voluntarios.

Está basado en el código de Carreros_ e inspirado en la idea de `escrutinio social`_,


.. _Carreros: https://github.com/concristina/carreros
.. _Escrutinio Social: https://github.com/democraciaconcodigos/escrutiniosocial

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











