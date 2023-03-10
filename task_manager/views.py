"""Views module"""
from django.shortcuts import render


def index(request):
    """Home page"""
    context = {'message': 'Hello, Hexlet!'}
    return render(request, 'index.html', context)
