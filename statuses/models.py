"""Statuses app models module"""
from django.db import models


class Status(models.Model):
    """Status model"""

    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        """Defines verbose names for Status objects"""
        verbose_name = 'Task status'

    def __str__(self):
        return f'Status: {self.name}'
