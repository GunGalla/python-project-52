"""Users app views module"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.mixins import CheckUserPermissionMixin, DeleteProtectionMixin


class UsersView(ListView):
    """Users list page"""

    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UsersCreate(SuccessMessageMixin, CreateView):
    """Views, related to users creation"""

    model = User
    form_class = UserRegistrationForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')
    extra_context = {
        'title': _('Registration'),
        'button': _('Register'),
    }


class UserUpdate(CheckUserPermissionMixin, SuccessMessageMixin, UpdateView):
    """Edit user's data."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'form.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully changed')
    extra_context = {
        'title': _('User update'),
        'button': _('Update'),
    }


class UserDelete(DeleteProtectionMixin, CheckUserPermissionMixin,
                 SuccessMessageMixin, DeleteView):
    """Delete user"""

    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully deleted')
    error_url = reverse_lazy('users:index')
    error_message = _('User has related objects, cannot delete.')
