"""Admin setup module for labels app"""
from django.contrib import admin
from .models import Label

admin.site.register(Label)
