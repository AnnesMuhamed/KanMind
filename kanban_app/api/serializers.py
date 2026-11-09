from rest_framework import serializers
from  kanban_app.models import Task
from kanban_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'priority', 'due_date', 'assigned_to', 'reviewer']

