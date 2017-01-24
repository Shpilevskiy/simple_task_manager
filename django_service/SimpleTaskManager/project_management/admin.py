from django.contrib import admin

from project_management.models import (
    Project,
    Task
)

admin.site.register(Project)
admin.site.register(Task)
