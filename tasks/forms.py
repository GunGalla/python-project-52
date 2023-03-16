"""Django forms module."""
from django.forms import ModelForm, CharField, Textarea
from django.utils.translation import gettext_lazy as _

from tasks.models import Task


class TaskCreationForm(ModelForm):
    """Class to create form for user creation."""
    class Meta:
        """Base settings"""
        model = Task
        fields = ['name', 'description', 'status', 'user', 'tag']

    name = CharField(label=_('Name'))
