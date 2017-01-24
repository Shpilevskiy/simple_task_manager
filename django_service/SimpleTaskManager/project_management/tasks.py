from __future__ import absolute_import, unicode_literals
from celery import shared_task

from SimpleTaskManager.celery import app


@app.task
def power(n):
    return 2 ** n
