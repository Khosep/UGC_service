#!/bin/bash

poetry run python manage.py migrate --noinput
poetry run python manage.py collectstatic --noinput
poetry run uwsgi --strict --ini uwsgi.ini

exec "$@"
