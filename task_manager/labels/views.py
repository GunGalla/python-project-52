"""labels app views module"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelCreationForm
from task_manager.mixins import DeleteProtectionMixin, CheckLoginMixin


class LabelsView(CheckLoginMixin, SuccessMessageMixin, ListView):
    """labels list page"""

    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelCreateView(CheckLoginMixin, SuccessMessageMixin, CreateView):
    """Views, related to label creation"""

    model = Label
    form_class = LabelCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button': _('Create'),
    }


class LabelUpdateView(CheckLoginMixin, SuccessMessageMixin, UpdateView):
    """Edit label data."""

    model = Label
    form_class = LabelCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully changed')
    extra_context = {
        'title': _('Update label'),
        'button': _('Update'),
    }


class LabelDeleteView(CheckLoginMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):
    """Delete label"""

    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully deleted')
    error_message = _('Label has related objects, cannot delete.')
    error_url = reverse_lazy('labels:index')
