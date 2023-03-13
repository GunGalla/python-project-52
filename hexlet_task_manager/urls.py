"""Urls of the project"""
from django.contrib import admin
from django.urls import path
from task_manager import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('users/<int:id>/update/', views.UserUpdate.as_view(), name='upd_user'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create', views.UsersCreate.as_view(), name='create'),
    path('admin/', admin.site.urls),
]
