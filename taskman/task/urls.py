from django.urls import path
from .views import TaskListView, TaskDetailView, TaskUpdateView, TaskDeleteView, TaskCreateView

urlpatterns = [
    path('home/', TaskListView.as_view(), name='task-home'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='task-detail'),
    path('task/update/<int:pk>', TaskUpdateView.as_view(), name='task-update'),
    path('task/delete/<int:pk>', TaskDeleteView.as_view(), name='task-delete'),
    path('task/create/', TaskCreateView.as_view(), name='task-create')
]