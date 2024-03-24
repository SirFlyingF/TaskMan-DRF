from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, CharField, DateTimeField
from django.contrib.auth.models import User
from  .models import Task


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TaskListSerializer(ModelSerializer):
    user = UserSerializer()
    # user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user']


class TaskCreateSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user']


class TaskDestroySerializer(ModelSerializer):
    class Meta:
        model = Task

    
class TaskSerializer(ModelSerializer):
    title = CharField(read_only=True)
    created_at = DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'created_at', 'user']
