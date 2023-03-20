"""Statuses app views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError

from statuses.models import Status
from statuses.forms import StatusCreationForm


class StatusesView(LoginRequiredMixin, View):
    """Statuses list page"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Getting all registered statuses"""
        statuses = Status.objects.all()
        context = {'statuses': statuses}
        if statuses:
            return render(request, 'statuses/statuses.html', context)
        else:
            return render(request, 'statuses/statuses.html')


class StatusCreate(LoginRequiredMixin, View):
    """Views, related to statuses creation"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows status creation form"""

        form = StatusCreationForm()
        context = {'form': form}
        return render(request, 'statuses/status_create.html', context)

    def post(self, request, *args, **kwargs):
        """Sends status creation form"""

        form = StatusCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return HttpResponseRedirect(reverse_lazy('statuses:index'))
        context = {'form': form}
        return render(request, 'statuses/status_create.html', context)


class StatusUpdate(LoginRequiredMixin, View):
    """Edit status data."""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows status form to further update"""

        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)

        form = StatusCreationForm(instance=status)
        context = {'form': form, 'status_id': status_id}
        return render(request, 'statuses/status_update.html', context)

    def post(self, request, *args, **kwargs):
        """Sends updated status info"""

        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusCreationForm(request.POST, instance=status)

        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully changed'))
            return HttpResponseRedirect(reverse_lazy('statuses:index'))
        context = {'form': form}
        return render(request, 'statuses/status_update.html', context)


class StatusDelete(LoginRequiredMixin, View):
    """Delete status"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        context = {'status': status}

        return render(request, 'statuses/status_delete.html', context)

    def post(self, request, *args, **kwargs):
        """Delete status"""
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)

        try:
            status.delete()
            messages.success(request, _('Status successfully deleted'))
            return HttpResponseRedirect(reverse_lazy('statuses:index'))
        except ProtectedError:
            messages.error(request, _('Status has related objects, cannot delete.'))
            return HttpResponseRedirect(reverse_lazy('statuses:index'))
