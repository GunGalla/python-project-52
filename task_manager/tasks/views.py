"""Tasks app views module"""
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.tasks.forms import TaskCreationForm
from task_manager.mixins import DelTaskPermissionMixin, CheckLoginMixin
from .filter import TaskFilter


class TasksView(CheckLoginMixin, FilterView):
    """tasks list page"""

    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskView(CheckLoginMixin, DetailView):
    """Current task page"""

    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'


class TaskCreateView(CheckLoginMixin, SuccessMessageMixin, CreateView):
    """Views, related to task creation"""

    model = Task
    template_name = 'form.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')
    extra_context = {
        'title': _('Create task'),
        'button': _('Create'),
    }

    def form_valid(self, form):
        """Set author of the task"""
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(CheckLoginMixin, SuccessMessageMixin, UpdateView):
    """Edit task data."""

    model = Task
    template_name = 'form.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully changed')
    extra_context = {
        'title': _('Update task'),
        'button': _('Update'),
    }


class TaskDeleteView(CheckLoginMixin, DelTaskPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    """Delete task"""

    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully deleted')
