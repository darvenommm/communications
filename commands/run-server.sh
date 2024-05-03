#!/bin/bash

poetry run python manage.py migrate
poetry run python manage.py createsuperuser --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL} --no-input
poetry run python manage.py runserver 0.0.0.0:${SERVER_PORT}
