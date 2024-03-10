# forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput

from .models import *


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['name', 'description', 'members']


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'space']


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name', 'folder', 'space']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'team', 'xp_reward', 'statuses', 'overall_status', 'tags']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    statuses = forms.ModelMultipleChoiceField(
        queryset=Status.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    # Add an additional field for the new overall status input
    tags = forms.CharField(max_length=255, required=False, help_text='Enter tags separated by commas')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-group'})

# class TaskForm(forms.ModelForm):
    # class Meta:
        # model = Task
        # fields = ['title', 'description', 'project', 'list', 'assignees', 'followers', 'assigned_to', 'due_date', 'updated_at', 'completed_at', 'tags', 'xp_reward', 'parent_task', 'dependency', 'progress', 'is_archived', , 'repeat_interval', 'reminder', 'is_private', 'custom_fields', 'priority', 'difficulty', 'position', 'status']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'due_date', 'priority', 'difficulty', 'list', 'assignees', 'tags', 'parent_task','dependency','repeat_interval','reminder','is_private']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.SelectMultiple(attrs={'class': 'select2'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        # You can customize other fields in a similar manner if needed


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'project', 'xp_reward', 'category', 'assigned_to']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'color']  # Include 'color' in fields

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Customize the form fields
        self.fields['profile_picture'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        self.fields['profile_picture'].label = 'Profile Picture'
        self.fields['profile_picture'].required = False

        # Add color picker to 'color'
        self.fields['color'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'id': 'color-picker', 'type': "color"})
        self.fields['color'].label = 'Avatar Color'
        self.fields['color'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['task', 'author', 'content']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['task', 'file', 'uploaded_by']