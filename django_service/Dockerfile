FROM python:3.6

ADD ./requirements.txt /api/requirements.txt
ADD ./docker-entrypoint.sh /api/
ADD ./run_celery.sh /api/

WORKDIR /api/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' apiuser

WORKDIR /api/SimpleTaskManager/
#ENTRYPOINT ["/api/docker-entrypoint.sh"]