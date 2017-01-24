#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# run Celery worker for our project with Celery configuration stored in Celeryconf
su -m apiuser -c "celery worker -A SimpleTaskManager.celery -Q default -n default@%h"