"""Users app views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from users.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UsersView(View):
    """Users list page"""

    def get(self, request, *args, **kwargs):
        """Getting all registered users"""
        users = User.objects.all()
        if users:
            return render(request, 'users/users.html', context={'users': users})
        else:
            return render(request, 'users/users.html')


class UsersCreate(View):
    """Views, related to users creation"""

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


class UserUpdate(View):
    """Edit user's data."""

    def get(self, request, *args, **kwargs):
        """Shows user form to further update"""

        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)

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
        user = User.objects.get(id=user_id)
        form = UserRegistrationForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully changed'))
            return HttpResponseRedirect(reverse_lazy('users:index'))
        context = {'form': form}
        return render(request, 'users/user_create.html', context)


class UserDelete(View):
    """Delete user"""

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)

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
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, _('User successfully deleted'))
        return HttpResponseRedirect(reverse_lazy('users:index'))
