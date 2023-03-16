"""Urls of the project"""
from django.contrib import admin
from django.urls import path, include
from task_manager.views import IndexView, Login, Logout

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/', include('users.urls', namespace='users')),
    path('statuses/', include('statuses.urls', namespace='statuses')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('admin/', admin.site.urls),
]
