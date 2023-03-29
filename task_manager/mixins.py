"""Mixins module"""
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class DelTaskPermissionMixin:
    """
    Check is current user author of the task and protect task deletion if not
    """
    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        if request.user.id != self.get_object().author.id:
            messages.error(
                request, _('Only author can delete task')
            )
            return HttpResponseRedirect(reverse_lazy('tasks:index'))
        return super().get(request, *args, **kwargs)


class CheckUserPermissionMixin:
    """Check is user authenticated"""
    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please, complete log in.')
            )
            return HttpResponseRedirect(reverse_lazy('login'))

        if request.user.id != self.get_object().id:
            messages.error(
                request, _('You have no permission to change other users')
            )
            return HttpResponseRedirect(reverse_lazy('users:index'))
        return super().get(request, *args, **kwargs)


class DeleteProtectionMixin:
    """Protect from deletion if object has related items"""
    error_message = ''
    error_url = ''

    def post(self, request, *args, **kwargs):
        """Delete label"""
        if self.get_object().tasks.count() > 0:
            messages.error(request, self.error_message)
            return HttpResponseRedirect(self.error_url)
        return super().post(request, *args, **kwargs)
