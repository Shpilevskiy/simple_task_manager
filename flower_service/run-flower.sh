#!/bin/bash
# wait for MQ server to start
sleep 10
celery --loglevel=info flower --address=0.0.0.0 --port=5555 --broker_api=http://guest:guest@messagequeue:15672/api/ --broker=amqp://guest:guest@messagequeue:5672//