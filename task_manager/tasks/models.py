"""Tasks app models module"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User


class Task(models.Model):
    """Status model"""

    author = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name=_('author')
    )

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))

    description = models.TextField(
        max_length=5000, null=True, blank=True, verbose_name=_('Description')
    )

    status = models.ForeignKey(
        to=Status,
        on_delete=models.PROTECT,
        related_name=_('status'),
        verbose_name=_('Status')
    )

    executor = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name=_('executor'),
        verbose_name=_('Executor')
    )

    labels = models.ManyToManyField(
        to=Label,
        related_name=_('tasks'),
        verbose_name=_('Labels'),
        blank=True,
    )

    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        """Defines verbose names for Task objects"""
        verbose_name = 'Task'

    def __str__(self):
        return f'{self.name}'
