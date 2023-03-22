"""Django forms module."""
from django.forms import ModelForm

from tasks.models import Task


class TaskCreationForm(ModelForm):
    """Class to create form for user creation."""

    def __init__(self, *args, **kwargs):
        """Changing form label"""
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = lambda obj:\
            f"{obj.first_name} {obj.last_name}"

    class Meta:
        """Base settings"""
        model = Task
        fields = ['name', 'description', 'status', 'user', 'label']
