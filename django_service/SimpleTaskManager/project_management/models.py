from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    members = models.ManyToManyField(User)


class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=2500)
    due_date = models.DateField()
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='tasks',
                                related_query_name='task')

    performer = models.OneToOneField(User, on_delete=models.CASCADE)
