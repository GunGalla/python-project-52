"""Tasks app urls"""
from django.urls import path

from tasks.views import (
    TasksView,
    TaskUpdateView,
    TaskCreateView,
    TaskDeleteView,
    TaskView,
)

app_name = 'tasks'

urlpatterns = [
    path('', TasksView.as_view(), name='index'),
    path('<int:id>/update/', TaskUpdateView.as_view(), name='upd_tasks'),
    path('<int:id>/delete/', TaskDeleteView.as_view(), name='del_tasks'),
    path('<int:id>', TaskView.as_view(), name='task'),
    path('create', TaskCreateView.as_view(), name='create'),
]
