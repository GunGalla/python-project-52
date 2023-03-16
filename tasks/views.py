"""Tasks app views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from tasks.forms import TaskCreationForm


class TasksView(LoginRequiredMixin, View):
    """tasks list page"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Getting all registered tasks"""
        tasks = Task.objects.all()
        context = {'tasks': tasks}
        if tasks:
            return render(request, 'tasks/tasks.html', context)
        else:
            return render(request, 'tasks/tasks.html')


class TaskCreate(LoginRequiredMixin, View):
    """Views, related to task creation"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows task creation form"""

        form = TaskCreationForm()
        context = {'form': form}
        return render(request, 'tasks/task_create.html', context)

    def post(self, request, *args, **kwargs):
        """Sends task creation form"""

        form = TaskCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('task successfully created'))
            return HttpResponseRedirect(reverse_lazy('tasks:index'))
        context = {'form': form}
        return render(request, 'tasks/task_create.html', context)


class TaskUpdate(LoginRequiredMixin, View):
    """Edit task data."""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows task form to further update"""

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)

        form = TaskCreationForm(instance=task)
        context = {'form': form, 'task_id': task_id}
        return render(request, 'tasks/task_update.html', context)

    def post(self, request, *args, **kwargs):
        """Sends updated task info"""

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskCreationForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, _('task successfully changed'))
            return HttpResponseRedirect(reverse_lazy('tasks:index'))
        context = {'form': form}
        return render(request, 'tasks/task_create.html', context)


class TaskDelete(LoginRequiredMixin, View):
    """Delete task"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        context = {'task': task}

        return render(request, 'tasks/task_delete.html', context)

    def post(self, request, *args, **kwargs):
        """Delete task"""
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.success(request, _('task successfully deleted'))
        return HttpResponseRedirect(reverse_lazy('tasks:index'))
