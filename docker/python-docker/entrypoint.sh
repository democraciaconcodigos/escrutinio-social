#!/bin/bash

if [ ! -f /project/escrutinio_social/local_settings.py ]; then
  cat /tmp/local-settings-docker.py >> /project/escrutinio_social/local_settings.py
else
  if ! cat /project/escrutinio_social/local_settings.py | grep "DATABASES"; then
    echo "DATABASES = {" >> /project/escrutinio_social/local_settings.py
    echo "    'default': {" >> /project/escrutinio_social/local_settings.py
    echo "        'ENGINE': 'django.db.backends.postgresql'," >> /project/escrutinio_social/local_settings.py
    echo "        'NAME': 'escrutinio_social'," >> /project/escrutinio_social/local_settings.py
    echo "        'USER': 'escrutinio'," >> /project/escrutinio_social/local_settings.py
    echo "        'PASSWORD': 'development'," >> /project/escrutinio_social/local_settings.py
    echo "        'HOST': 'db'," >> /project/escrutinio_social/local_settings.py
    echo "        'PORT': '5432'," >> /project/escrutinio_social/local_settings.py
    echo "    }" >> /project/escrutinio_social/local_settings.py
    echo "}" >> /project/escrutinio_social/local_settings.py
  fi
  if ! cat /project/escrutinio_social/local_settings.py | grep "GOOGLE_ANALYTICS_PROPERTY_ID"; then
    echo "GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-345678-2'" >> /project/escrutinio_social/local_settings.py
  fi
fi

echo "Installing required packages" \
 && pip3 install -r /project/requirements.txt \
 && echo "Packages installation finished" \
 && python3.6 /project/manage.py migrate \
 && python3.6 /project/manage.py loaddata fixtures/* \
 && python3.6 /project/manage.py runserver 0.0.0.0:8000 \
