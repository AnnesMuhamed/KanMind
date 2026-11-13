from rest_framework import serializers
from kanban_app.models import Board, Task, Comment



class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Resolves the author's name automatically using a read-only field source.
    """
    author_name = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_name', 'text', 'created_at']


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for the Board model, handling board details and creation timestamps.
    """
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model, managing all task-related fields including
    status, priority, assignments, reviewers, and due dates with explicit field mapping.
    """
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assigned_to', 'reviewer', 'due_date', 'created_at']