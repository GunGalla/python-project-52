"""Tasks app models module"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from statuses.models import Status
from labels.models import Label


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

    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name=_('executor'),
        verbose_name=_('User')
    )

    label = models.ManyToManyField(
        to=Label,
        related_name=_('label'),
        verbose_name=_('Label'),
    )

    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        """Defines verbose names for Status objects"""
        verbose_name = 'Task'

    def __str__(self):
        return {self.name}
