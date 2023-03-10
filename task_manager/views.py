"""Views module"""
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User


class IndexView(View):
    """Home page"""

    def get(self, request, *args, **kwargs):
        """Home page"""
        return render(request, 'index.html')


class UsersView(View):
    """Urers list page"""

    def get(self, request, *args, ** kwargs):
        """Getting all registered users"""
        users = User.objects.all()
        if users:
            return render(request, 'users.html', context= {'users': users})
        else:
            return render(request, 'users.html')
