"""Users app urls"""
from django.urls import path

from task_manager.users.views import (
    UsersView,
    UserUpdate,
    UsersCreate,
    UserDelete
)

app_name = 'users'

urlpatterns = [
    path('', UsersView.as_view(), name='index'),
    path('<int:id>/update/', UserUpdate.as_view(), name='upd_user'),
    path('<int:id>/delete/', UserDelete.as_view(), name='del_user'),
    path('create/', UsersCreate.as_view(), name='create'),
]
