from django.conf.urls import url

from project_management.views import (
    UsersListCreateView,
    UserRetrieveUpdateDestroy
)

from SimpleTaskManager.utils.url_kwargs_consts import USER_URL_KWARG

urlpatterns = [
    url(r'^users/(?P<{}>[0-9]+)'.format(USER_URL_KWARG), UserRetrieveUpdateDestroy.as_view(), name='users'),
    url(r'^users/', UsersListCreateView.as_view(), name='users')
]