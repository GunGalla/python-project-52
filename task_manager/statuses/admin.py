"""Admin module in statuses app"""
from django.contrib import admin
from .models import Status

admin.site.register(Status)
