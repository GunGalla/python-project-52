"""Views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
# from django.utils.translation import gettext_lazy as _

from .forms import UserLoginForm


class IndexView(View):
    """Home page"""

    def get(self, request, *args, **kwargs):
        """Home page"""
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        """Home page"""
        return render(request, 'index.html')


class Login(View):
    """Log in views class"""

    def get(self, request, *args, **kwargs):
        """Shows login screen"""
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        """Auth"""
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request, username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('index'))

        else:
            form = UserLoginForm()
        return render(request, 'login.html', context={'form': form})


class Logout(View):
    """Logging out class"""

    def post(self, request, *args, **kwargs):
        """Logging out of site"""
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))
