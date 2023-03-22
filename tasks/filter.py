"""Filter module"""
from django_filters import ModelChoiceFilter, BooleanFilter, FilterSet
from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from labels.models import Label
from users.models import User


class TaskFilter(FilterSet):
    """Task filter setup."""
    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
    )
    author = BooleanFilter(
        widget=CheckboxInput,
        label=_('Only my tasks'),
    )

    user = ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('User'),
        to_field_name='id',

    )

    class Meta:
        """Base fields"""
        model = Task
        fields = ['status', 'user', 'label']
