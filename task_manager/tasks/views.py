"""Tasks app views module"""
from django.shortcuts import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.tasks.forms import TaskCreationForm
from .filter import TaskFilter


class TasksView(LoginRequiredMixin, FilterView):
    """tasks list page"""
    login_url = reverse_lazy('login')

    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskView(LoginRequiredMixin, DetailView):
    """Current task page"""
    login_url = reverse_lazy('login')

    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Views, related to task creation"""
    login_url = reverse_lazy('login')

    model = Task
    template_name = 'tasks/task_create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        """Set author of the task"""
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit task data."""
    login_url = reverse_lazy('login')

    model = Task
    template_name = 'tasks/task_update.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully changed')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete task"""
    login_url = reverse_lazy('login')

    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully deleted')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        if request.user.id != task.author.id:
            messages.error(
                request, _('Only author can delete task')
            )
            return HttpResponseRedirect(reverse_lazy('tasks:index'))

        return super().get(request, *args, **kwargs)
