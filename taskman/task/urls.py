from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDestroyView, TaskUpdateView, TaskDetailView

urlpatterns = [
    path('api/home/', TaskListView.as_view(), name='api-task-home'),
    path('api/create/', TaskCreateView.as_view(), name='api-task-create'),
    path('api/delete/<int:pk>', TaskDestroyView.as_view(), name='api-task-delete'),
    path('api/update/<int:pk>', TaskUpdateView.as_view(), name='api-task-update'),
    path('api/home/<int:pk>', TaskDetailView.as_view(), name='api-task-detail'),
]