"""Django forms module."""
from django.forms import ModelForm, CharField
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusCreationForm(ModelForm):
    """Class to create form for user creation."""
    class Meta:
        """Base settings"""
        model = Status
        fields = ['name']

    name = CharField(label=_('Name'))
