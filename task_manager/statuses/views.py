"""Statuses app views module"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreationForm
from task_manager.mixins import DeleteProtectionMixin


class StatusesView(LoginRequiredMixin, ListView):
    """Statuses list page"""
    login_url = reverse_lazy('login')

    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Views, related to statuses creation"""
    login_url = reverse_lazy('login')

    model = Status
    form_class = StatusCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully created')
    extra_context = {
        'title': _('Create status'),
        'button': _('Create'),
    }


class StatusUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit status data."""
    login_url = reverse_lazy('login')

    model = Status
    form_class = StatusCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully changed')
    extra_context = {
        'title': _('Update status'),
        'button': _('Update'),
    }


class StatusDelete(LoginRequiredMixin, DeleteProtectionMixin,
                   SuccessMessageMixin, DeleteView):
    """Delete status"""
    login_url = reverse_lazy('login')

    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully deleted')
    error_url = reverse_lazy('statuses:index')
    error_message = _('Status has related objects, cannot delete.')
