"""Tasks app views module"""
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from tasks.forms import TaskCreationForm
from .filter import TaskFilter


class TasksView(LoginRequiredMixin, View):
    """tasks list page"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Getting all registered tasks"""
        tasks = Task.objects.all()
        f = TaskFilter(request.GET, tasks)

        status = request.GET.get('status')
        labels = request.GET.get('labels')
        executor = request.GET.get('executor')
        author = request.GET.get('author')

        if status:
            tasks = tasks.filter(status__id=status)

        if labels:
            tasks = tasks.filter(labels__id=labels)

        if executor:
            tasks = tasks.filter(executor__id=executor)

        if author:
            tasks = tasks.filter(author__id=request.user.id)

        context = {'tasks': tasks, 'filter': f}
        if tasks:
            return render(request, 'tasks/tasks.html', context)
        else:
            return render(request, 'tasks/tasks.html', context={'filter': f})


class TaskView(LoginRequiredMixin, View):
    """Current task page"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Getting distinct task"""
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        context = {'task': task}
        return render(request, 'tasks/task.html', context)


class TaskCreateView(LoginRequiredMixin, View):
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
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, _('task successfully created'))
            return HttpResponseRedirect(reverse_lazy('tasks:index'))
        context = {'form': form}
        return render(request, 'tasks/task_create.html', context)


class TaskUpdateView(LoginRequiredMixin, View):
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
            messages.success(request, 'Задача успешно изменена')
            return HttpResponseRedirect(reverse_lazy('tasks:index'))
        context = {'form': form}
        return render(request, 'tasks/task_update.html', context)


class TaskDeleteView(LoginRequiredMixin, View):
    """Delete task"""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Shows alert and delete confirmation"""

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        context = {'task': task}
        if request.user.id == task.author.id:
            return render(request, 'tasks/task_delete.html', context)

        messages.error(
            request, _('Only author can delete task')
        )
        return HttpResponseRedirect(reverse_lazy('tasks:index'))

    def post(self, request, *args, **kwargs):
        """Delete task"""
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.success(request, 'Задача уcпешно удалена')
        return HttpResponseRedirect(reverse_lazy('tasks:index'))
