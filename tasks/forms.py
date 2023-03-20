"""Django forms module."""
from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
    SelectMultiple,
)
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from labels.models import Label


class TaskCreationForm(ModelForm):
    """Class to create form for user creation."""
    class Meta:
        """Base settings"""
        model = Task
        fields = ['name', 'description', 'status', 'user', 'label']
