"""Django forms module."""
from django.forms import ModelForm

from tasks.models import Task


class TaskCreationForm(ModelForm):
    """Class to create form for user creation."""

    class Meta:
        """Base settings"""
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
