#!/bin/bash

if [ ! -f /project/escrutiniociudadano/local_settings.py ]; then
  cat /tmp/local-settings-docker.py >> /project/escrutiniociudadano/local_settings.py
else
  if ! cat /project/escrutiniociudadano/local_settings.py | grep "DATABASES"; then
    echo "DATABASES = {" >> /project/escrutiniociudadano/local_settings.py
    echo "    'default': {" >> /project/escrutiniociudadano/local_settings.py
    echo "        'ENGINE': 'django.db.backends.postgresql'," >> /project/escrutiniociudadano/local_settings.py
    echo "        'NAME': 'escrutiniociudadano'," >> /project/escrutiniociudadano/local_settings.py
    echo "        'USER': 'escrutinio'," >> /project/escrutiniociudadano/local_settings.py
    echo "        'PASSWORD': 'development'," >> /project/escrutiniociudadano/local_settings.py
    echo "        'HOST': 'db'," >> /project/escrutiniociudadano/local_settings.py
    echo "        'PORT': '5432'," >> /project/escrutiniociudadano/local_settings.py
    echo "    }" >> /project/escrutiniociudadano/local_settings.py
    echo "}" >> /project/escrutiniociudadano/local_settings.py
  fi
  if ! cat /project/escrutiniociudadano/local_settings.py | grep "GOOGLE_ANALYTICS_PROPERTY_ID"; then
    echo "GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-345678-2'" >> /project/escrutiniociudadano/local_settings.py
  fi
fi

echo "Installing required packages" \
 && pip3 install -r /project/requirements.txt \
 && echo "Packages installation finished" \
 && python3.6 /project/manage.py migrate \
 && python3.6 /project/manage.py loaddata fixtures/* \
 && python3.6 /project/manage.py runserver 0.0.0.0:8000 \
