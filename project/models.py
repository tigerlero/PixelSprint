# models.py
import random
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='grey')

    def __str__(self):
        return self.name


class Space(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='spaces', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=100)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    color = models.CharField(max_length=7, default='#00ff00')  # Default color is green

    def generate_random_dark_color(self):
        # Generate a random hex color in the dark color range
        dark_color_range = list(range(0, 128))  # Adjust the range as needed
        random_color = "#{:02x}{:02x}{:02x}".format(
            random.choice(dark_color_range),
            random.choice(dark_color_range),
            random.choice(dark_color_range)
        )
        return random_color

    def update_xp(self):
        # Get the last status ID
        last_status_id = Status.objects.aggregate(last_id=Max('id'))['last_id']
        # Calculate XP from completed tasks with the last status ID
        completed_tasks_xp = sum(task.xp_reward for task in self.assigned_tasks.filter(status=last_status_id))

        # Update the user's XP
        self.xp = completed_tasks_xp
        self.save()

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile.objects.create(user=instance)
            profile.color = profile.generate_random_dark_color()
            profile.save()
        instance.userprofile.update_xp()


class Status(models.Model):
    # THIS IS FOR WHICH STATUS IS WHICH TASK AND WHAT COLOR THE COLUMN AND A PROJECT HAS SET FROM STATUSES
    name = models.CharField(max_length=50, unique=False)
    color = models.CharField(max_length=20)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='statuses')
    def __str__(self):
        return f"{self.name} - {self.color}"


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    team = models.ManyToManyField(User, related_name='projects')
    xp_reward = models.PositiveIntegerField(default=2)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    # Add a OneToOneField to represent the overall project status
    overall_status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='projects', null=True, blank=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=1)
    assignees = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    followers = models.ManyToManyField(User, related_name='followed_tasks', blank=True)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_tasks', unique=False)
    due_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    estimated_time = models.DurationField(blank=True, null=True)
    actual_time = models.DurationField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='tasks', blank=True)
    xp_reward = models.PositiveIntegerField(default=1)
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subtasks', null=True, blank=True)
    dependency = models.ManyToManyField('self', symmetrical=False, related_name='dependent_tasks', blank=True)
    progress = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    repeat_interval = models.CharField(max_length=50, blank=True, null=True)
    reminder = models.DateTimeField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    custom_fields = models.JSONField(blank=True, null=True)
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
    position = models.PositiveIntegerField(default=0)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='tasks', default=1)

    def save(self, *args, **kwargs):

        if self.pk is not None:
            original_task = Task.objects.get(pk=self.pk)
            if original_task.project != self.project:
                # Update Status reference for the old project
                original_status = Status.objects.get(
                    name=original_task.status.name,
                    project=original_task.project
                )
                original_status.project = self.project
                original_status.save()
        # Calculate xp_reward based on priority and difficulty
        priority_multiplier = {
            'Critical': 4,
            'High': 3,
            'Medium': 2,
            'Low': 1,
        }

        difficulty_multiplier = {
            'Easy': 1,
            'Medium': 2,
            'Hard': 3,
            'Very Hard': 4,
            'Extreme': 5,
        }

        xp_reward = int(priority_multiplier.get(self.priority, 1) * difficulty_multiplier.get(self.difficulty, 1))

        # Set calculated xp_reward before saving
        self.xp_reward = xp_reward

        super().save(*args, **kwargs)
        self.assigned_to.update_xp()

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


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - Uploaded by {self.uploaded_by.username}"