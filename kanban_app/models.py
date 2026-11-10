"""
Database models for the Kanban application.
Defines structures for Boards, Contacts, Tasks, and Comments with clean relationships.
"""

from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Represents a Kanban board containing multiple tasks.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    """
    Represents a person or team member who can be assigned to tasks
    or author comments, optionally linked to a Django user account.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a Kanban task within a board, tracking status, priority,
    assigned contacts, reviewers, and due dates.
    """

    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks') 
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    assigned_to = models.ManyToManyField(Contact, related_name='assigned_tasks', blank=True)
    reviewer = models.ForeignKey(Contact, related_name='reviewed_tasks', on_delete=models.SET_NULL, null=True, blank=True)

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a text comment written by a contact on a specific task.
    """
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.name} on {self.task.title}"