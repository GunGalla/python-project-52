"""Statuses app views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from users.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusesView(LoginRequiredMixin, View):
    """Users list page"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Getting all registered users"""
        statuses = Status.objects.all()
        if statuses:
            return render(request, 'statuses/statuses.html', context={'statuses': statuses})
        else:
            return render(request, 'statuses/statuses.html')


class StatusCreate(LoginRequiredMixin, View):
    """Views, related to users creation"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows user creation form"""

        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'users/user_create.html', context)

    def post(self, request, *args, **kwargs):
        """Sends user creation form"""

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully registered'))
            return HttpResponseRedirect(reverse_lazy('login'))
        context = {'form': form}
        return render(request, 'users/user_create.html', context)


class StatusUpdate(LoginRequiredMixin, View):
    """Edit user's data."""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows user form to further update"""

        user_id = kwargs.get('id')
        user = Status.objects.get(id=user_id)

        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please, complete log in.')
            )
            return HttpResponseRedirect(reverse_lazy('login'))

        if request.user.id == user.id:
            form = UserRegistrationForm(instance=user)
            context = {'form': form, 'user_id': user_id}
            return render(request, 'users/user_create.html', context)

        messages.error(
            request, _('You have no permission to change other users')
        )
        return HttpResponseRedirect(reverse_lazy('users:index'))

    def post(self, request, *args, **kwargs):
        """Sends updated user info"""
        user_id = kwargs.get('id')
        user = Status.objects.get(id=user_id)
        form = UserRegistrationForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully changed'))
            return HttpResponseRedirect(reverse_lazy('users:index'))
        context = {'form': form}
        return render(request, 'users/user_create.html', context)


class StatusDelete(LoginRequiredMixin, View):
    """Delete user"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        user_id = kwargs.get('id')
        user = Status.objects.get(id=user_id)

        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please, complete log in.')
            )
            return HttpResponseRedirect(reverse_lazy('login'))

        if request.user.id == user.id:
            return render(request, 'users/user_delete.html')

        messages.error(
            request, _('You have no permission to change other users')
        )
        return HttpResponseRedirect(reverse_lazy('users:index'))

    def post(self, request, *args, **kwargs):
        """Delete user"""
        user_id = kwargs.get('id')
        user = Status.objects.get(id=user_id)
        user.delete()
        messages.success(request, _('User successfully deleted'))
        return HttpResponseRedirect(reverse_lazy('users:index'))

