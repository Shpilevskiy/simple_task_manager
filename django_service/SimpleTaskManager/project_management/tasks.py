from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.utils import timezone

from SimpleTaskManager.settings import EMAIL_HOST_USER

from SimpleTaskManager.celery import app

from project_management.models import Task


@app.task
def send_email_task(title, body, recipient):
    send_mail(
        title,
        body,
        EMAIL_HOST_USER,
        [recipient])


@app.task
def send_reminder_emails():
    tasks = Task.objects.filter(due_date=timezone.now().date())
    for task in tasks:
        body = 'Task: {}\n Description: {}'.format(task.title, task.description)
        send_email_task.delay(
            "The task expires today!",
            body,
            task.performer.email
        )
