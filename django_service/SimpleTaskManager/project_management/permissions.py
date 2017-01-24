from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)

from project_management.models import Project

from SimpleTaskManager.utils.groups_consts import MANAGER_GROUP
from SimpleTaskManager.utils.url_kwargs_consts import PROJECT_URL_KWARG


class IsManagerUser(BasePermission):
    # Only managers have Read and Write permissions
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name=MANAGER_GROUP):
            return True
        return False


class IsManagerOrReadOnly(BasePermission):
    # Read permissions are allowed for everyone
    # Write permissions are allowed only for managers.
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.groups.filter(name=MANAGER_GROUP):
            return True
        return False


class IsManagerOrProjectMemberReadOnly(BasePermission):
    # Read permissions are allowed for the project members or managers,
    # Write permissions are allowed for any manager.
    def has_permission(self, request, view):
        project_id = request.parser_context['kwargs'].get(PROJECT_URL_KWARG)
        if project_id is None:
            return False
        if request.user.is_staff or request.user.groups.filter(name=MANAGER_GROUP):
            return True
        if request.method in SAFE_METHODS:
            try:
                project = Project.objects.get(id=project_id)
                return project.is_member(request.user)
            except Project.DoesNotExist:
                return False
        return False
