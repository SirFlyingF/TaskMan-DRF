# Generated by Django 5.0.3 on 2024-03-23 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], default='To Do', max_length=20),
        ),
    ]
