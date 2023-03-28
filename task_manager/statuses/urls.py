"""Statuses app urls"""
from django.urls import path

from task_manager.statuses.views import (
    StatusesView,
    StatusUpdate,
    StatusCreate,
    StatusDelete,
)

app_name = 'statuses'

urlpatterns = [
    path('', StatusesView.as_view(), name='index'),
    path('<int:pk>/update/', StatusUpdate.as_view(), name='upd_status'),
    path('<int:pk>/delete/', StatusDelete.as_view(), name='del_status'),
    path('create/', StatusCreate.as_view(), name='create'),
]
