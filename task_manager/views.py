"""Views module"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from task_manager.forms import UserRegistrationForm, UserLoginForm
from django.utils.translation import gettext_lazy as _


class IndexView(View):
    """Home page"""

    def get(self, request, *args, **kwargs):
        """Home page"""
        return render(request, 'index.html')
    
    def post(self, request, *args, **kwargs):
        """Home page"""
        return render(request, 'index.html')


class UsersView(View):
    """Users list page"""

    def get(self, request, *args, **kwargs):
        """Getting all registered users"""
        users = User.objects.all()
        if users:
            return render(request, 'users.html', context={'users': users})
        else:
            return render(request, 'users.html')


class UsersCreate(View):
    """Views, related to users creation"""

    def get(self, request, *args, **kwargs):
        """Shows user creation form"""

        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'user_create.html', context)

    def post(self, request, *args, **kwargs):
        """Sends user creation form"""

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        context = {'form': form}
        return render(request, 'user_create.html', context)


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
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('index')

        else:
            form = UserLoginForm()
        return render(request, 'login.html', context={'form': form})


class Logout(View):
    """Logging out class"""

    def post(self, request, *args, **kwargs):
        """Logging out of site"""
        auth.logout(request)
        return redirect('index')
