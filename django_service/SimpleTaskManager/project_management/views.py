from django.contrib.auth.models import User

from rest_framework import (
    generics,
    permissions
)

from project_management.serializers import (
    UserSerializer
)


class UsersListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
