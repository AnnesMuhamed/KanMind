"""
URL configuration for the Kanban app API endpoints.
Maps endpoints for boards, tasks, contacts, and comments to their respective generic views.
"""

from django.urls import path
from kanban_app.api.views import (
    AssignedToMeTaskListAPIView,
    BoardListCreateAPIView,
    BoardRetrieveUpdateDestroyAPIView,
    ReviewingTaskListAPIView,
    TaskCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentDestroyAPIView,
    EmailCheckAPIView
)

urlpatterns = [
    path('boards/', BoardListCreateAPIView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardRetrieveUpdateDestroyAPIView.as_view(), name='board-detail'),

        path('email-check/', EmailCheckAPIView.as_view(), name='email-check'),

    path('tasks/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/assigned-to-me/', AssignedToMeTaskListAPIView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', ReviewingTaskListAPIView.as_view(), name='tasks-reviewing'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),

    path('tasks/<int:task_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('tasks/<int:task_id>/comments/<int:pk>/', CommentDestroyAPIView.as_view(), name='comment-delete'),
]
