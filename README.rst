Escrutinio Social
=================

.. image:: https://travis-ci.org/democraciaconcodigos/escrutinio-social.svg?branch=master
   :target: https://travis-ci.org/democraciaconcodigos/escrutinio-social


.. info:: Este fue el repositorio original del proyecto, nacido en el evento "Democracia con códigos" en Córdoba, 2013. El desarrollo vigente lo impulsa el colectivo Open Data Córdoba y el repositorio es https://github.com/OpenDataCordoba/escrutinio-social


Escrutinio Social es una plataforma web para un recuento provisorio de resultados electorales basado en la colaboración de voluntari@s.


Es una iniciativa de `Open Data Córdoba <https://github.com/OpenDataCordoba>`_ junto a diversas organizaciones
sociales y políticas, con el fin de incrementar la transparencia y fortalecer la democracia.


Cómo funciona
--------------

La plataforma permite asociar diversa documentación donde conste el resultado de una mesa (fotos de actas de la mesa provista
por fiscales o el presidente de mesa, fotos de actas partidarias firmadas por otros fiscales, digitalizacion de telegramas provistos
por la justicia electoral)

Esa documentación se "sube" via web/app (por ejemplo se las envia a una dirección de email asociada al sistema) y voluntarios la catalogan para indicar de qué mesa se trata. Luego, el mismo u otro voluntario se encargará de digitalizar los resultados en una interfaz fácil de usar por cualquiera, desde una PC o celular.

Al voluntari@ le van llegando documentos de mesas a cargar que el propio sistema va priorizando, en funcion de las actas disponibles y la informacion ya relevada. Los datos que se releven se pueden contrastar con los oficiales a medida que estén disponibles.


Sumate al proyecto
------------------

Este proyecto está en fase de desarrollo y hay mucho por hacer. ¡Queremos usarlo en las proximas elecciones del 22 de octubre!. Hace falta gente que sepa programar y diseñar, periodistas, usuarios de redes sociales y cualquiera que quiera "cargar" antes, durante y después de las elecciones de octubre!

Tenemos un canal chat en Slack donde debatimos ideas, novedades y "organizamos" el trabajo. Podés `sumarte a través de este link <https://join.slack.com/t/escrutiniosocial/shared_invite/MjQxMjMyOTMwMTYwLTE1MDU0OTIxMjgtN2VhOWE1ZDg4ZQ>`_ y luego ingresar a https://escrutiniosocial.slack.com/

En la wiki_ desarrollamos documentación (tanto técnica como no técnica).

.. _wiki: https://github.com/democraciaconcodigos/escrutiniosocial/wiki


Entorno de desarrollo con Docker
--------------------------------

Este es un proyecto basado en Django y cuenta con la configuracion de docker para levantar los servicios en contenedores.

Para levantar el proyecto necesitamos contar con docker (https://docs.docker.com/engine/installation/) y docker-compose (https://docs.docker.com/compose/install/).

  `Se recomienda seguir los pasos post instalación para poder ejecutar docker sin utilizar el usuario root.`

Una vez instaladas las dependencias debemos entrar en la carpeta de docker y ejecutar `docker-compose up`.

.. code:: bash

  docker-compose up -d

Para inicializar la base de datos por primera vez, se deberá ejecutar:

.. code:: bash

  docker-compose run app init

Luego de finalizado el proceso podrán acceder a través de `http://localhost/`.

Un superusuario ``admin`` con clave ``admin`` se habrá cargado

Entorno de desarrollo - Instalación tradicional
-----------------------------------------------

Es un proyecto basado en Django. Requiere Python 3.6 y Postgresql.
Podés ver este `tutorial <https://tutorial.djangogirls.org/es/django_installation/>`_
para instrucciones detalladas de como instalar Django con python 3.6.

1. Crear un virtualenv
2. ``pip install -r requirements.txt``
3. crear base de datos postgres y configurar los datos en ``escrutinio_social/settings.py``

4. ``python manage.py migrate``
5. cargar fixtures ``python manage.py loaddata fixtures/*``
6. ``python manage.py runserver``

Un superusuario ``admin`` con clave ``admin`` se habrá cargado
