"""Tasks app urls"""
from django.urls import path

from task_manager.tasks.views import (
    TasksView,
    TaskUpdateView,
    TaskCreateView,
    TaskDeleteView,
    TaskView,
)

app_name = 'tasks'

urlpatterns = [
    path('', TasksView.as_view(), name='index'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='upd_tasks'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='del_tasks'),
    path('<int:pk>/', TaskView.as_view(), name='task'),
    path('create/', TaskCreateView.as_view(), name='create'),
]
