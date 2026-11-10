"""
URL configuration for the Kanban app API endpoints.
Maps endpoints for boards, tasks, contacts, and comments to their respective generic views.
"""

from django.urls import path
from kanban_app.api.views import (
    BoardListCreateAPIView, 
    BoardRetrieveUpdateDestroyAPIView, 
    TaskListCreateAPIView, 
    TaskRetrieveUpdateDestroyAPIView,
    ContactListCreateAPIView,
    ContactRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView
    )

urlpatterns = [
    path('boards/', BoardListCreateAPIView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardRetrieveUpdateDestroyAPIView.as_view(), name='board-detail'),
    
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    
    path('contacts/', ContactListCreateAPIView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactRetrieveUpdateDestroyAPIView.as_view(), name='contact-detail'),
    
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
]