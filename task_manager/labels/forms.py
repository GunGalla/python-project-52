"""Django forms module."""
from django.forms import ModelForm, CharField
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


class LabelCreationForm(ModelForm):
    """Class to create form for user creation."""
    class Meta:
        """Base settings"""
        model = Label
        fields = ['name']

    name = CharField(label=_('Name'))
