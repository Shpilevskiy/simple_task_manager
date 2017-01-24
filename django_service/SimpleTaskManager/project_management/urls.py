from django.conf.urls import url

from project_management.views import (
    UsersListCreateView
)

urlpatterns = [
    url(r'^users/', UsersListCreateView.as_view(), name='users')
]