from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import UserProfile, Project, Task, Note
from .forms import ProjectForm, TaskForm, NoteForm, UserProfileForm
from itertools import groupby
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Task

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Change 'home' to the name of your home page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # Change 'home' to the name of your home page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def homepage(request):
    return render(request, 'homepage.html')


# UserProfile views
def create_userprofile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('userprofile_list'))
    else:
        form = UserProfileForm()

    return render(request, 'userprofile_form.html', {'form': form})


def update_userprofile(request, userprofile_id):
    userprofile = get_object_or_404(UserProfile, id=userprofile_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=userprofile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('userprofile_list'))
    else:
        form = UserProfileForm(instance=userprofile)

    return render(request, 'userprofile_form.html', {'form': form})


# UserProfile views
def userprofile_list(request):
    userprofiles = UserProfile.objects.all()
    return render(request, 'userprofile_list.html', {'userprofiles': userprofiles})


def userprofile_detail(request, userprofile_id):
    userprofile = get_object_or_404(UserProfile, id=userprofile_id)
    return render(request, 'userprofile_detail.html', {'userprofile': userprofile})


# Project views
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})


def create_or_update_project(request, project_id=None):
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    else:
        project = None

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'project_form.html', {'form': form})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm()

    return render(request, 'project_form.html', {'form': form})


def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm(instance=project)

    return render(request, 'project_form.html', {'form': form})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return HttpResponseRedirect(reverse('project_list'))

    return render(request, 'project_confirm_delete.html', {'project': project})


# Task views
def task_list(request):
    # Fetch tasks from the database and group them by status
    tasks = Task.objects.all()
    task_statuses = {}
    for status, _ in Task.STATUS_CHOICES:
        task_statuses[status] = tasks.filter(status=status)

    # Add other context data as needed

    return render(request, 'task_list.html', {'task_statuses': task_statuses, 'form': TaskForm()})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})




def create_task(request, status):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = status
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task_list'))
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect(reverse('task_list'))

    return render(request, 'task_confirm_delete.html', {'task': task})


# Note views


def note_list(request):
    # Assuming you have a queryset of Note objects
    notes = Note.objects.all().order_by('assigned_to', 'project')

    # Grouping notes by assigned_to and project
    grouped_notes = {}
    for (assigned_to, project), group in groupby(notes, key=lambda note: (note.assigned_to, note.project)):
        grouped_notes.setdefault(assigned_to, {}).setdefault(project, []).extend(group)

    return render(request, 'note_list.html', {'grouped_notes': grouped_notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'note_detail.html', {'note': note})


def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('note_list'))
    else:
        form = NoteForm()

    return render(request, 'note_form.html', {'form': form})


def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('note_list'))
    else:
        form = NoteForm(instance=note)

    return render(request, 'note_form.html', {'form': form})


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        note.delete()
        return HttpResponseRedirect(reverse('note_list'))

    return render(request, 'note_confirm_delete.html', {'note': note})
