from rest_framework import viewsets
from kanban_app.models import Task
from kanban_app.api.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
