"""Tasks app models module"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from statuses.models import Status


class Task(models.Model):
    """Status model"""

    author = models.ForeignKey(to=User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    description = models.TextField(max_length=5000, null=True, blank=True)
    status = models.ForeignKey(to=Status, on_delete=models.PROTECT,
                               related_name='status')
    user = models.ForeignKey(to=User, on_delete=models.PROTECT,
                             null=True, blank=True, related_name='Executor')
    tag = models.ForeignKey(to=Status, on_delete=models.PROTECT,
                            null=True, blank=True, related_name='tag')
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        """Defines verbose names for Status objects"""
        verbose_name = 'Task'

    def __str__(self):
        return f'Status: {self.name}'
