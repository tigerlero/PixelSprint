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


from django.db import models

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
    position = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    due_date = models.DateField()
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

    def save(self, *args, **kwargs):
        # Calculate xp_reward based on priority and difficulty
        priority_multiplier = {
            'Critical': 3,
            'High': 2,
            'Medium': 1,
            'Low': 1,  # You can adjust this as needed
        }

        difficulty_multiplier = {
            'Easy': 1,   # You can adjust this as needed
            'Medium': 1,
            'Hard': 2,
            'Very Hard': 3,
            'Extreme': 4,
        }

        xp_reward = int(priority_multiplier.get(self.priority, 1) * difficulty_multiplier.get(self.difficulty, 1))

        # Set calculated xp_reward before saving
        self.xp_reward = xp_reward

        super().save(*args, **kwargs)

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
