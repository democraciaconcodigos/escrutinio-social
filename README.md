escrutiniosocial
================

[![Build Status](https://travis-ci.org/democraciaconcodigos/escrutiniosocial.png?branch=master)](https://travis-ci.org/democraciaconcodigos/escrutiniosocial)

Una aplicación web para validar colaborativamente el escrutinio provisorio


Para cargar datos oficiales a partir de los csv publicados:

1. Cargar información de provincias y departamentos:
    $ python manage.py cargar_provincias electoral-2013-departamentos.csv

2. Cargar información de partidos:
    $ python manage.py cargar_partidos electoral-2013-partidos.csv

3. Cargar datos de resultados:
    $ python manage.py cargar_eleccion "Diputados nacionales" electoral-2013-diputados_nacionales.csv



Para colaborar con el proyecto:

1. Forkear el proyecto en tu cuenta de github
2. Clonar el fork desde la terminal con
    $ git clone (url de tu fork, proyecto en tu github)
3. Desde la terminal agregar el repo original
    $ git remote add upstream

Algunas cosas útiles:
### $ git push origin master
Pushes commits to your remote repository stored on GitHub
### $ git fetch upstream
Fetches any new changes from the original repository
### $ git merge upstream/master
Merges any changes fetched into your working files
### $ git branch mybranch
Creates a new branch called "mybranch"
### $ git checkout mybranch
Makes "mybranch" the active branch
### $ git checkout master
Makes "master" the active branch
### $ git merge mybranch
Merges the commits from "mybranch" into "master"
###$ git branch -d mybranch
Deletes the "mybranch" branch

visit https://help.github.com/articles/using-pull-requests
to learn how to send your contribution to the original repo.
