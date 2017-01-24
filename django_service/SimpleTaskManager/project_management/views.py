from django.contrib.auth.models import User

from rest_framework import (
    generics,
    permissions
)
from rest_framework import status
from rest_framework.response import Response

from project_management.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    ProjectSerializer,
    ProjectMembersSerializer,
    TaskSerializer,
    TaskPerformerSerializer
)

from project_management.models import (
    Project,
    Task
)
from project_management.permissions import (
    IsManagerUser,
    IsManagerOrReadOnly,
    IsManagerOrProjectMemberReadOnly
)

from SimpleTaskManager.utils.url_kwargs_consts import (
    USER_URL_KWARG,
    PROJECT_URL_KWARG,
    TASK_URL_KWARG
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
    permission_classes = (permissions.IsAuthenticated, IsManagerOrReadOnly)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerOrReadOnly)
    lookup_url_kwarg = PROJECT_URL_KWARG

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectMembersSerializer
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs[PROJECT_URL_KWARG])


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerOrProjectMemberReadOnly)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs[PROJECT_URL_KWARG])

    def get(self, request, *args, **kwargs):
        if Project.objects.filter(id=kwargs[PROJECT_URL_KWARG]).exists():
            return super().get(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Project is not found."})

    def post(self, request, *args, **kwargs):
        if Project.objects.filter(id=kwargs[PROJECT_URL_KWARG]).exists():
            return super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Project is not found."})


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerOrProjectMemberReadOnly)
    serializer_class = TaskSerializer
    lookup_url_kwarg = TASK_URL_KWARG

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskPerformerSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            project_id=self.kwargs[PROJECT_URL_KWARG],
            id=self.kwargs[TASK_URL_KWARG]
        )
