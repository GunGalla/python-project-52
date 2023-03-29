"""labels app views module"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelCreationForm
from task_manager.mixins import DeleteProtectionMixin


class LabelsView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    """labels list page"""
    login_url = reverse_lazy('login')

    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Views, related to label creation"""
    login_url = reverse_lazy('login')

    model = Label
    form_class = LabelCreationForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit label data."""
    login_url = reverse_lazy('login')

    model = Label
    form_class = LabelCreationForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully changed')


class LabelDeleteView(LoginRequiredMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):
    """Delete label"""
    login_url = reverse_lazy('login')

    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully deleted')
    error_message = _('Label has related objects, cannot delete.')
    error_url = reverse_lazy('labels:index')
