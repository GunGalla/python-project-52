"""labels app views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError

from labels.models import Label
from labels.forms import LabelCreationForm


class LabelsView(LoginRequiredMixin, View):
    """labels list page"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Getting all registered labels"""
        labels = Label.objects.all()
        context = {'labels': labels}
        if labels:
            return render(request, 'labels/labels.html', context)
        else:
            return render(request, 'labels/labels.html')


class LabelCreateView(LoginRequiredMixin, View):
    """Views, related to label creation"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows label creation form"""

        form = LabelCreationForm()
        context = {'form': form}
        return render(request, 'labels/label_create.html', context)

    def post(self, request, *args, **kwargs):
        """Sends label creation form"""

        form = LabelCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully created'))
            return HttpResponseRedirect(reverse_lazy('labels:index'))
        context = {'form': form}
        return render(request, 'labels/label_create.html', context)


class LabelUpdateView(LoginRequiredMixin, View):
    """Edit label data."""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows label form to further update"""

        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)

        form = LabelCreationForm(instance=label)
        context = {'form': form, 'label_id': label_id}
        return render(request, 'labels/label_update.html', context)

    def post(self, request, *args, **kwargs):
        """Sends updated label info"""

        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelCreationForm(request.POST, instance=label)

        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully changed'))
            return HttpResponseRedirect(reverse_lazy('labels:index'))
        context = {'form': form}
        return render(request, 'labels/label_update.html', context)


class LabelDeleteView(LoginRequiredMixin, View):
    """Delete label"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        context = {'label': label}

        return render(request, 'labels/label_delete.html', context)

    def post(self, request, *args, **kwargs):
        """Delete label"""
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)

        try:
            label.delete()
            messages.success(request, _('Label successfully deleted'))
            return HttpResponseRedirect(reverse_lazy('labels:index'))
        except ProtectedError:
            messages.error(request, _(
                'Label has related objects, cannot delete.'
            ))
            return HttpResponseRedirect(reverse_lazy('labels:index'))
