"""Statuses app views module"""
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreationForm


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
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully created')


class StatusUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit status data."""
    login_url = reverse_lazy('login')

    model = Status
    form_class = StatusCreationForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully changed')


class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete status"""
    login_url = reverse_lazy('login')

    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully deleted')

    def post(self, request, *args, **kwargs):
        """Delete status"""
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _(
                'Status has related objects, cannot delete.'
            ))
            return HttpResponseRedirect(reverse_lazy('statuses:index'))
