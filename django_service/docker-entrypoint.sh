#!/bin/sh
# wait for PostgreSQl server to start
sleep 10
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata fixtures
echo "from django.contrib.auth.models import User; User.objects.create_superuser('adminadmin', 'admin@example.com', 'adminadmin')" | python manage.py shell
su -m apiuser -c "gunicorn -b :8000 -w 4  SimpleTaskManager.wsgi:application --reload"

