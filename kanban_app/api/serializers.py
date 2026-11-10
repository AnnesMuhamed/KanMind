from rest_framework import serializers
from  kanban_app.models import Task
from kanban_app.models import Board, Task, Contact, Comment


class ContactSerializer(serializers.ModelSerializer):
    initials = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'user', 'initials']

    def get_initials(self, obj):
        if not obj.name:
            return ""
        names = obj.name.split()
        if len(names) >= 2:
            return (names[0][0] + names[-1][0]).upper()
        elif len(names) == 1:
            return names[0][:2].upper()
        return ""

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_name', 'text', 'created_at']

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
