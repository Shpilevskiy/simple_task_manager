#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
su -m apiuser -c "gunicorn -b :8000 -w 4  SimpleTaskManager.wsgi:application --reload"

