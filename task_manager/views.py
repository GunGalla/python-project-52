"""Views module"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from task_manager.forms import UserRegistrationForm


class IndexView(View):
    """Home page"""

    def get(self, request, *args, **kwargs):
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
        """Shows log in page"""
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        """Auth"""
        redirect('index')
