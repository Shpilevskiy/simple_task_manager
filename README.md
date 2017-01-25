# Simple task Manager

## Requirements:
 - docker
 - python
 - pip
 - git
 
## How to launch:
 - git clone https://github.com/Shpilevskiy/simple_task_manager.git
 - cd simple_task_manager
 - sudo pip install -r requirements.txt
 - docker-compose up --build

## What we have got:
 - Nginx - http://127.0.0.1:8080/
 - Django application - http://127.0.0.1:8080/api/ (default SU username/password: adminadmin)
 - RabbitMQ management - http://127.0.0.1:15672/ (username/password: guest)
 - Celery flower - http://127.0.0.1:5555/
 - postgresql
 - scalable celery workers
 - redis
