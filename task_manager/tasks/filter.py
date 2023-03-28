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
        method='get_only_my_tasks',
    )

    def get_only_my_tasks(self, queryset, name, value):
        """Filter tasks by author"""
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        """Base fields"""
        model = Task
        fields = ['status', 'executor']
