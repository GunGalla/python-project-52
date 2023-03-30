"""Mixins module"""
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class DelTaskPermissionMixin:
    """
    Check is current user author of the task and protect task deletion if not
    """
    def dispatch(self, request, *args, **kwargs):
        """Check if current user author of the task"""
        if request.user.id != self.get_object().author.id:
            messages.error(request, _('Only author can delete task'))
            return HttpResponseRedirect(reverse_lazy('tasks:index'))
        return super().dispatch(request, *args, **kwargs)


class CheckLoginMixin(UserPassesTestMixin):
    """Check is user authenticated"""
    def test_func(self):
        """Check if user logged in"""
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        """Redirect to log in page if there are no user logged in"""
        messages.error(
            self.request, _('You are not authorized! Please, complete log in.')
        )
        return HttpResponseRedirect(reverse_lazy('login'))


class CheckUserPermissionMixin:
    """Only user can update or delete himself check"""

    def dispatch(self, request, *args, **kwargs):
        """Check if user has permission to update or delete object"""
        if request.user.id != self.get_object().id:
            messages.error(
                request, _('You have no permission to change other users')
            )
            return HttpResponseRedirect(reverse_lazy('users:index'))
        return super().dispatch(request, *args, **kwargs)


class DeleteProtectionMixin:
    """Protect from deletion if object has related items"""
    error_message = ''
    error_url = ''

    def post(self, request, *args, **kwargs):
        """Delete label"""
        if self.get_object().tasks.exists():
            messages.error(request, self.error_message)
            return HttpResponseRedirect(self.error_url)
        return super().post(request, *args, **kwargs)
