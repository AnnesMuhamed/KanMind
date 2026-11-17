from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kanban_app.api.permissions import (
    IsBoardOwnerOrMember,
    IsCommentAuthor,
    IsTaskBoardMember,
)
from kanban_app.api.serializers import (
    BoardDetailSerializer,
    BoardListSerializer,
    BoardUpdateSerializer,
    CommentSerializer,
    TaskSerializer,
    UserSerializer,
)
from kanban_app.models import Board, Comment, Task


class BoardListCreateAPIView(generics.ListCreateAPIView):
    """Lists the boards of the user and creates new boards."""
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns only boards the user owns or is a member of."""
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        """Saves the new board with the current user as owner."""
        serializer.save(owner=self.request.user)


class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Shows, updates or deletes a single board."""
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated & IsBoardOwnerOrMember]

    def get_serializer_class(self):
        """Returns the serializer that fits the request method."""
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    """Creates a task on a board the user belongs to."""
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsBoardOwnerOrMember]

    def create(self, request, *args, **kwargs):
        """Checks that the board exists and the user may use it."""
        board_id = request.data.get('board')
        if isinstance(board_id, int):
            board = get_object_or_404(Board, pk=board_id)
            self.check_object_permissions(request, board)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Saves the task with the current user as creator."""
        serializer.save(created_by=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Updates or deletes a single task."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsTaskBoardMember]


class AssignedToMeTaskListAPIView(generics.ListAPIView):
    """Lists all tasks assigned to the current user."""
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns only tasks where the user is the assignee."""
        return Task.objects.filter(assignee=self.request.user)


class ReviewingTaskListAPIView(generics.ListAPIView):
    """Lists all tasks the current user has to review."""
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns only tasks where the user is the reviewer."""
        return Task.objects.filter(reviewer=self.request.user)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """Lists and creates the comments of a task."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & IsTaskBoardMember]

    def get_task(self):
        """Returns the task from the URL and checks the permission."""
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        self.check_object_permissions(self.request, task)
        return task

    def get_queryset(self):
        """Returns all comments of the task."""
        return self.get_task().comments.all()

    def perform_create(self, serializer):
        """Saves the comment with its task and the current user as author."""
        serializer.save(task=self.get_task(), author=self.request.user)


class CommentDestroyAPIView(generics.DestroyAPIView):
    """Deletes a comment of a task."""
    permission_classes = [IsAuthenticated & IsCommentAuthor]

    def get_queryset(self):
        """Returns only comments of the task from the URL."""
        return Comment.objects.filter(task=self.kwargs['task_id'])


class EmailCheckAPIView(APIView):
    """Returns the user with the given email address."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Checks the email and returns the matching user."""
        email = request.query_params.get('email')
        if not email or '@' not in email:
            return Response(
                {'email': 'A valid email address is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)
