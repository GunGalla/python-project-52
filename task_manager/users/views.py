"""Users app views module"""
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError

from task_manager.users.models import User


class UsersView(ListView):
    """Users list page"""

    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UsersCreate(SuccessMessageMixin, CreateView):
    """Views, related to users creation"""

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdate(SuccessMessageMixin, UpdateView):
    """Edit user's data."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully changed')

    def get(self, request, *args, **kwargs):
        """Shows user form to further update"""

        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please, complete log in.')
            )
            return HttpResponseRedirect(reverse_lazy('login'))

        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)

        if request.user.id != user.id:
            messages.error(
                request, _('You have no permission to change other users')
            )
            return HttpResponseRedirect(reverse_lazy('users:index'))
        return super().get(request, *args, **kwargs)


class UserDelete(SuccessMessageMixin, DeleteView):
    """Delete user"""

    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully deleted')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please, complete log in.')
            )
            return HttpResponseRedirect(reverse_lazy('login'))

        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)

        if request.user.id != user.id:
            messages.error(
                request, _('You have no permission to change other users')
            )
            return HttpResponseRedirect(reverse_lazy('users:index'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Delete user"""
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _(
                'User has related objects, cannot delete.'
            ))
            return HttpResponseRedirect(reverse_lazy('users:index'))
