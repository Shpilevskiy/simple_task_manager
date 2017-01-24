from django.contrib.auth.models import User

from rest_framework import (
    generics,
    permissions
)

from project_management.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    ProjectSerializer,
    ProjectMembersSerializer
)

from project_management.models import (
    Project,
    Task
)
from project_management.permissions import IsManagerUser

from SimpleTaskManager.utils.url_kwargs_consts import (
    USER_URL_KWARG,
    PROJECT_URL_KWARG
)


class UsersListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerUser)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerUser)
    serializer_class = UserUpdateSerializer
    lookup_url_kwarg = USER_URL_KWARG

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs[USER_URL_KWARG])


class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerUser)
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectMembersSerializer
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerUser)
    lookup_url_kwarg = PROJECT_URL_KWARG

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectMembersSerializer
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs[PROJECT_URL_KWARG])
