from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=128, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)