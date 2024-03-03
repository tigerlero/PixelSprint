# forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput

from .models import Project, Task, Note, UserProfile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'team', 'xp_reward', 'status']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'due_date', 'priority', 'difficulty']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        # You can customize other fields in a similar manner if needed


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'project', 'xp_reward', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
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
        self.fields['profile_picture'].widget = forms.ClearableFileInput(attrs={'class': 'form-control' })
        self.fields['profile_picture'].label = 'Profile Picture'
        self.fields['profile_picture'].required = False

        # Add color picker to 'color'
        self.fields['color'].widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'color-picker', 'type':"color" })
        self.fields['color'].label = 'Avatar Color'
        self.fields['color'].required = False
