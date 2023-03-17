"""Labels app urls"""
from django.urls import path

from labels.views import (
    LabelsView,
    LabelUpdateView,
    LabelCreateView,
    LabelDeleteView,
)

app_name = 'labels'

urlpatterns = [
    path('', LabelsView.as_view(), name='index'),
    path('<int:id>/update/', LabelUpdateView.as_view(), name='upd_label'),
    path('<int:id>/delete/', LabelDeleteView.as_view(), name='del_label'),
    path('create', LabelCreateView.as_view(), name='create'),
]
