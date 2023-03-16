"""Tasks app urls"""
from django.urls import path

from tasks.views import (
    TasksView,
    TaskUpdate,
    TaskCreate,
    TaskDelete,
)

app_name = 'tasks'

urlpatterns = [
    path('', TasksView.as_view(), name='index'),
    path('<int:id>/update/', TaskUpdate.as_view(), name='upd_tasks'),
    path('<int:id>/delete/', TaskDelete.as_view(), name='del_tasks'),
    path('create', TaskCreate.as_view(), name='create'),
]
