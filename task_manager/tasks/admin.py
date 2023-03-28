"""Admin setup module for tasks app"""
from django.contrib import admin
from .models import Task

admin.site.register(Task)
