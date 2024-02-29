# models.py

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    team = models.ManyToManyField(User, related_name='projects')
    xp_reward = models.PositiveIntegerField(default=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Backlog', 'Backlog'),
            ('Sprint Planning', 'Sprint Planning'),
            ('In Progress', 'In Progress'),
            ('Code Review', 'Code Review'),
            ('Testing', 'Testing'),
            ('Done', 'Done'),
        ],
        default='Backlog'
    )

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Review', 'Review'),
        ('Testing', 'Testing'),
        ('Done', 'Done'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='To Do'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    xp_reward = models.PositiveIntegerField(default=1)
    priority = models.CharField(
        max_length=20,
        choices=[
            ('Critical', 'Critical'),
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Low', 'Low'),
        ],
        default='Medium'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
            ('Very Hard', 'Very Hard'),
            ('Extreme', 'Extreme'),
        ],
        default='Medium'
    )

    def __str__(self):
        return self.title


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    xp_reward = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=50, blank=True, null=True)
    assigned_to = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
