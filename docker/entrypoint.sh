#!/bin/bash

set -eoux pipefail

if [ "$1" == 'init' ]; then
    echo "Inicializar base de datos"
    ${SITE_DIR}/env/bin/python ${SITE_DIR}/proj/manage.py migrate
    ${SITE_DIR}/env/bin/python ${SITE_DIR}/proj/manage.py collectstatic --no-input
    ${SITE_DIR}/env/bin/python ${SITE_DIR}/proj/manage.py loaddata ${SITE_DIR}/proj/fixtures/*
elif [ "$1" == 'manage' ]; then
    shift
    echo "Manage.py $@"
    ${SITE_DIR}/env/bin/python ${SITE_DIR}/proj/manage.py $@
else
    exec "$@"
fi