"""Statuses app models module"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Status model"""

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        """Defines verbose names for Status objects"""
        verbose_name = 'Task status'

    def __str__(self):
        return self.name
