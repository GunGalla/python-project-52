"""Labels app urls"""
from django.urls import path

from task_manager.labels.views import (
    LabelsView,
    LabelUpdateView,
    LabelCreateView,
    LabelDeleteView,
)

app_name = 'labels'

urlpatterns = [
    path('', LabelsView.as_view(), name='index'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='upd_label'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='del_label'),
    path('create/', LabelCreateView.as_view(), name='create'),
]
