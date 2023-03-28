# Generated by Django 4.1.7 on 2023-03-28 12:30

from django.db import migrations, models

# flake8: noqa
class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0004_rename_label_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='labels.label', verbose_name='Labels'),
        ),
    ]