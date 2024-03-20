from django.urls import path
from .views import listview

urlpatterns = [
    path('home/', listview, name='task-home')
]