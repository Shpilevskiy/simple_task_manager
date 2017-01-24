from django.conf.urls import url

from project_management.views import (
    UsersListCreateView,
    UserRetrieveUpdateDestroyView,
    ProjectListCreateView,
    ProjectRetrieveUpdateDestroyView
)

from SimpleTaskManager.utils.url_kwargs_consts import(
    USER_URL_KWARG,
    PROJECT_URL_KWARG
)

urlpatterns = [
    url(r'^users/(?P<{}>[0-9]+)'.format(USER_URL_KWARG), UserRetrieveUpdateDestroyView.as_view(), name='user'),
    url(r'^users/', UsersListCreateView.as_view(), name='users'),

    url(r'^projects/(?P<{}>[0-9]+)'.format(PROJECT_URL_KWARG), ProjectRetrieveUpdateDestroyView.as_view(), name='project'),
    url(r'^projects/', ProjectListCreateView.as_view(), name='projects')
]