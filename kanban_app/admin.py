from django.contrib import admin

from kanban_app.models import Board, Comment, Task


admin.site.register(Board)
admin.site.register(Comment)
admin.site.register(Task)
