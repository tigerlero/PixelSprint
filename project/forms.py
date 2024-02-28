# forms.py
from django import forms
from .models import Project, Task, Note


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'team', 'xp_reward', 'status']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'due_date', 'completed', 'xp_reward', 'priority',
                  'difficulty']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'project', 'xp_reward', 'category']
