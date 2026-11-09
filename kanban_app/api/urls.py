from django.urls import path
from kanban_app.api.views import (BoardListCreateAPIView, BoardRetrieveUpdateDestroyAPIView, TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView)

urlpatterns = [
    path('boards/', BoardListCreateAPIView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardRetrieveUpdateDestroyAPIView.as_view(), name='board-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
]