"""Filter module"""
from django_filters import ModelChoiceFilter, BooleanFilter, FilterSet
from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    """Task filter setup."""
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
    )
    author = BooleanFilter(
        widget=CheckboxInput,
        label=_('Only my tasks'),
    )

    class Meta:
        """Base fields"""
        model = Task
        fields = ['status', 'executor', 'labels']
