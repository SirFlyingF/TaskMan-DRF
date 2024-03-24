from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

STATUS_CHOICES = [
    'To Do',
    'In Progress',
    'Done',
]
choices_as_tuple = [(status, status) for status in STATUS_CHOICES]

class Task(models.Model):
    title = models.CharField(max_length=128, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=choices_as_tuple, default='To Do')