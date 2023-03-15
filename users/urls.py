"""Users app urls"""
from django.urls import path

from users.views import UsersView, UserUpdate, UsersCreate, UserDelete

app_name = 'users'

urlpatterns = [
    path('', UsersView.as_view(), name='index'),
    path('<int:id>/update/', UserUpdate.as_view(), name='upd_user'),
    path('<int:id>/delete/', UserDelete.as_view(), name='del_user'),
    path('users/create', UsersCreate.as_view(), name='create'),
]
