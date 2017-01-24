from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    members = models.ManyToManyField(User)

    def is_member(self, user):
        """
        Returns whether the given user instance
        is the member of the current project
        """
        return self.members.filter(id=user.id).exists()

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=2500)
    due_date = models.DateField()
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='tasks',
                                related_query_name='task')

    performer = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='tasks',
                                  related_query_name='task')

    def __str__(self):
        return self.title
