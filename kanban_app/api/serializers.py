from rest_framework import serializers
from kanban_app.models import Board, Task, Contact, Comment


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.
    Includes a custom method field to automatically generate initials from the contact's name.
    """
    initials = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'user', 'initials']

    def get_initials(self, obj):
        """
        Calculates and returns uppercase initials based on the contact's full name
        (e.g., 'John Doe' -> 'JD') for frontend UI rendering.
        """
        if not obj.name:
            return ""
        names = obj.name.split()
        if len(names) >= 2:
            return (names[0][0] + names[-1][0]).upper()
        elif len(names) == 1:
            return names[0][:2].upper()
        return ""


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