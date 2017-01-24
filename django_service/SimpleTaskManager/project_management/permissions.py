from rest_framework.permissions import BasePermission

from django.contrib.auth.models import Group

from SimpleTaskManager.utils.groups_consts import MANAGER_GROUP


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name=MANAGER_GROUP):
            return True
        return False
