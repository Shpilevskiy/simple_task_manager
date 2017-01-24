from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from SimpleTaskManager.settings import EMAIL_HOST_USER

from SimpleTaskManager.celery import app


@app.task
def send_email_task(title, body, recipient):
    send_mail(
        title,
        body,
        EMAIL_HOST_USER,
        [recipient])
