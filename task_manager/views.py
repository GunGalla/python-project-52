"""Views module"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext_lazy as _

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
                messages.success(request, _('You logged in'))
                return HttpResponseRedirect(reverse_lazy('index'))

        else:
            form = UserLoginForm()
            messages.error(request, _(
                'Please enter a correct username and password. '
                'Note that both fields may be case-sensitive.'
            ))
        return render(request, 'login.html', context={'form': form})


class Logout(View):
    """Logging out class"""

    def post(self, request, *args, **kwargs):
        """Logging out of site"""
        logout(request)
        messages.info(request, _('You logged out'))
        return HttpResponseRedirect(reverse_lazy('index'))


def index(request):
    a = None
    a.hello()  # Creating an error with an invalid line of code
    dsadfasf
    return HttpResponse("Hello, world. You're at the pollapp index.")
