# Generated by Django 4.1.7 on 2023-03-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0004_alter_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='label', to='labels.label', verbose_name='Label'),
        ),
    ]
