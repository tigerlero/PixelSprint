from django.contrib.auth.models import User
from django.db.models import Max, F
from django.shortcuts import render
import hashlib
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .models import UserProfile, Project, Task, Note
from .forms import ProjectForm, TaskForm, NoteForm, UserProfileForm
from itertools import groupby
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Task
from django.contrib.auth import logout

from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm  # Import your UserProfileForm


def gravatar_url(username, size=40):
    default = "https://example.com/default.jpg"  # URL of your default image
    username_hash = hashlib.md5(username.lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{username_hash}?d={default}&s={size}"


@login_required
def user_profile_form_view(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile_form')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'userprofile_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')  # Change this to the URL where you want to redirect after logout

# for user in User.objects.all():
#         UserProfile.objects.get_or_create(user=user)

def update_task_status(request, task_id, new_status, new_position):
    task = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        # Ensure the new_position is an integer
        try:
            new_position = int(new_position)
        except ValueError:
            return HttpResponseBadRequest('Invalid position value')

        # Save the old position for comparison
        old_position = task.position

        # Update task status and position
        task.status = new_status
        task.position = new_position
        task.save()

        # Update positions of other tasks in the same status
        if old_position < new_position:
            # Moving down
            Task.objects.filter(status=new_status, position__gt=old_position, position__lte=new_position).exclude(
                pk=task_id).update(position=F('position') - 1)
        elif old_position > new_position:
            # Moving up
            Task.objects.filter(status=new_status, position__lt=old_position, position__gte=new_position).exclude(
                pk=task_id).update(position=F('position') + 1)

        # Return a JSON response
        return JsonResponse({'message': 'Task status and position updated successfully', 'status': new_status,
                             'position': new_position})

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=400)


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
@login_required
def task_list(request, project_id=None):
    # Fetch tasks based on project_id if provided, otherwise fetch all tasks
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        tasks = Task.objects.filter(project=project).order_by('position', 'status').all()
    else:
        tasks = Task.objects.order_by('position', 'status').all()

    # Group tasks by status
    task_statuses = {}
    for status, _ in Task.STATUS_CHOICES:
        task_statuses[status] = tasks.filter(status=status)

    # Include profile picture information in the context
    user_profile_picture = request.user.userprofile.profile_picture if hasattr(request.user, 'userprofile') else None

    return render(request, 'task_list.html', {
        'task_statuses': task_statuses,
        'form': TaskForm(),
        'user_profile_picture': user_profile_picture,
    })


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def change_priority(request, task_id):
    task = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        new_priority = request.POST.get('priority')
        print(f"Received new priority: {new_priority}")  # Add this line to check if data is received correctly
        task.priority = new_priority
        task.save()
        print("Task priority updated successfully")  # Add this line to check if the task is saved successfully

    return redirect('task_list')


def create_task(request, status):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = status

            # Get the maximum position in the current status
            max_position = Task.objects.filter(status=status).aggregate(Max('position'))['position__max']

            # Set the new task's position to one greater than the maximum position
            task.position = max_position + 1 if max_position is not None else 1

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
