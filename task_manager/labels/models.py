"""Statuses app models module"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Label(models.Model):
    """Label model"""

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        """Defines verbose names for Status objects"""
        verbose_name = 'Label'

    def __str__(self):
        return f'{self.name}'
