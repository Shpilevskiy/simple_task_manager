from django.contrib.auth.models import User

from rest_framework import (
    generics,
    permissions
)

from project_management.serializers import (
    UserSerializer,
    UserUpdateSerializer
)

from SimpleTaskManager.utils.url_kwargs_consts import (
    USER_URL_KWARG
)

from project_management.permissions import IsManagerUser


class UsersListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerUser)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsManagerUser)
    serializer_class = UserUpdateSerializer
    lookup_url_kwarg = USER_URL_KWARG

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs[USER_URL_KWARG])
