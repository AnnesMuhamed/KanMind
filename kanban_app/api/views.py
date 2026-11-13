from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from kanban_app.models import Board, Comment, Task
from kanban_app.api.serializers import BoardSerializer, TaskSerializer, CommentSerializer


class BoardListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of all boards or create a new board.
    Requires authentication.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]


class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific board by ID.
    Requires authentication.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all tasks or create a new task.
    Requires authentication.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific task by ID.
    Requires authentication.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all comments or create a new comment.
    Requires authentication.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific comment by ID.
    Requires authentication.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]