"""Django forms module."""
from django.forms import ModelForm, ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from statuses.models import Status


class TaskCreationForm(ModelForm):
    """Class to create form for user creation."""
    class Meta:
        """Base settings"""
        model = Task
        fields = ['name', 'description', 'status', 'user', 'tag']

    # tag = ModelMultipleChoiceField(
    #     label=_('Tag'),
    #     queryset=Status.objects.all(),
    #     required=False,
    # )
