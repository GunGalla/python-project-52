"""Statuses app urls"""
from django.urls import path

from statuses.views import (
    StatusesView,
    StatusUpdate,
    StatusCreate,
    StatusDelete,
)

app_name = 'statuses'

urlpatterns = [
    path('', StatusesView.as_view(), name='index'),
    path('<int:id>/update/', StatusUpdate.as_view(), name='upd_status'),
    path('<int:id>/delete/', StatusDelete.as_view(), name='del_status'),
    path('statuses/create', StatusCreate.as_view(), name='create'),
]
