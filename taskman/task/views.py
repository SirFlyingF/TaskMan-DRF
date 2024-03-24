from .serializers import TaskListSerializer, TaskCreateSerializer, TaskDestroySerializer, TaskSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Task

# Create your views here.


class TaskCreateView(CreateAPIView):
    serializer_class = TaskCreateSerializer


class TaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()


class TaskDestroyView(DestroyAPIView):
    serializer_class = TaskDestroySerializer
    queryset = Task.objects.all()


class TaskUpdateView(UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDetailView(RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()