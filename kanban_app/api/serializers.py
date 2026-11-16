from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Task, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializes a user with id, email and full name."""
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """Returns the full name of the user."""
        return obj.get_full_name()


class BoardTaskSerializer(serializers.ModelSerializer):
    """Serializes a task with assignee and reviewer for the board view."""
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count',
        ]

    def get_comments_count(self, obj):
        """Returns the number of comments of the task."""
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Resolves the author's name automatically using a read-only field source.
    """
    author_name = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_name', 'text', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """Serializes a task and accepts assignee and reviewer by id."""
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee',
        write_only=True, required=False, allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer',
        write_only=True, required=False, allow_null=True,
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'assignee_id', 'reviewer_id',
            'due_date', 'comments_count',
        ]

    def get_comments_count(self, obj):
        """Returns the number of comments of the task."""
        return obj.comments.count()

    def validate(self, attrs):
        """Checks that assignee and reviewer are members of the board."""
        board = self.get_board(attrs)
        for field in ['assignee', 'reviewer']:
            user = attrs.get(field)
            if user and user not in board.members.all():
                raise serializers.ValidationError(
                    {f'{field}_id': 'User must be a member of the board.'}
                )
        return attrs

    def get_board(self, attrs):
        """Returns the board and prevents moving a task to another board."""
        board = attrs.get('board')
        if self.instance is None:
            return board
        if board is not None and board != self.instance.board:
            raise serializers.ValidationError(
                {'board': 'Changing the board is not allowed.'}
            )
        return self.instance.board


class BoardListSerializer(serializers.ModelSerializer):
    """Serializes a board with its counts for the board overview."""
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'members', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id'
        ]
        extra_kwargs = {'members': {'write_only': True}}

    def get_member_count(self, obj):
        """Returns the number of members of the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the number of all tasks of the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the number of tasks with the status to-do."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the number of tasks with the priority high."""
        return obj.tasks.filter(priority='high').count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializes a board with its members and tasks."""
    members = UserSerializer(many=True, read_only=True)
    tasks = BoardTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(serializers.ModelSerializer):
    """Updates the title and members of a board."""
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data', 'members']
        extra_kwargs = {'members': {'write_only': True}}