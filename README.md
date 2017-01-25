# Simple task Manager

## Requirements:
 - docker
 - python
 - pip
 - git
 - free 8080, 15672, 5432, 5555 ports
 
## How to launch:
 - git clone https://github.com/Shpilevskiy/simple_task_manager.git
 - cd simple_task_manager
 - sudo pip install -r requirements.txt
 - docker-compose up --build

## What we have got:
 - Nginx - http://127.0.0.1:8080/
 - Django application - http://127.0.0.1:8080/api/ (default SU username/password: adminadmin)
    - Managers managers have all CRUD rights for every endpoint.
    - Developers are allowed only safe methods
    - http://127.0.0.1:8080/api/api-auth/login/ - login page (change 'login' to 'logout' for logout)
    
    - http://127.0.0.1:8080/api/management/users/ - lists of all users and creating new user, only managers and SU can reach this endpoint
    - http://127.0.0.1:8080/api/management/users/1/ - changing, deleting, detailed information about specific user
    - http://127.0.0.1:8080/api/management/projects/ - list of all projects and creating new project, developers can use only safe methods
    - http://127.0.0.1:8080/api/management/projects/1/ - changing, deleting, detailed information about specific project, developers can use only safe methods
    - http://127.0.0.1:8080/api/management/projects/1/tasks/ - list of all tasks of the project, Only those developers who were added to the project can reach endpoint (save methods). when you create a task performer receives a letter on the email address that was specified at registration
    - http://127.0.0.1:8080/api/management/projects/1/tasks/1/ - changing, deleting, detailed information about specific task
 - RabbitMQ management - http://127.0.0.1:15672/ (username/password: guest)
 - Celery flower - http://127.0.0.1:5555/
 - postgresql :5432
 - scalable celery workers
 - redis :6379
