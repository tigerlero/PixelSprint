from django.contrib.auth.models import User
from django.db.models import *
from django.shortcuts import render
import hashlib
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from itertools import groupby
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


def list_list(request):
    lists = List.objects.all()
    return render(request, 'list_list.html', {'lists': lists})


def space_list(request):
    spaces = Space.objects.all()
    return render(request, 'space_list.html', {'spaces': spaces})


def folder_list(request):
    folders = Folder.objects.all()
    return render(request, 'folder_list.html', {'folders': folders})


def list_detail(request, list_id):
    list_obj = get_object_or_404(List, pk=list_id)
    return render(request, 'list_detail.html', {'list': list_obj})


def space_detail(request, space_id):
    space_obj = get_object_or_404(Space, pk=space_id)
    return render(request, 'space_detail.html', {'space': space_obj})


def folder_detail(request, folder_id):
    folder_obj = get_object_or_404(Folder, pk=folder_id)
    return render(request, 'folder_detail.html', {'folder': folder_obj})


def create_or_update_list(request, list_id=None):
    if list_id:
        list_obj = get_object_or_404(List, id=list_id)
    else:
        list_obj = None

    if request.method == 'POST':
        form = ListForm(request.POST, instance=list_obj)
        if form.is_valid():
            form.save()
            return redirect('list_list')
    else:
        form = ListForm(instance=list_obj)

    return render(request, 'list_form.html', {'form': form})


def create_or_update_space(request, space_id=None):
    if space_id:
        space = get_object_or_404(Space, id=space_id)
    else:
        space = None

    if request.method == 'POST':
        form = SpaceForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            return redirect('space_list')
    else:
        form = SpaceForm(instance=space)

    return render(request, 'space_form.html', {'form': form})


def create_or_update_folder(request, folder_id=None):
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id)
    else:
        folder = None

    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('folder_list')
    else:
        form = FolderForm(instance=folder)

    return render(request, 'folder_form.html', {'form': form})


def delete_list(request, list_id):
    list_obj = List.objects.get(pk=list_id)
    list_obj.delete()
    return redirect('list_deleted')


def delete_space(request, space_id):
    space_obj = Space.objects.get(pk=space_id)
    space_obj.delete()
    return redirect('space_deleted')


def delete_folder(request, folder_id):
    folder_obj = Folder.objects.get(pk=folder_id)
    folder_obj.delete()
    return redirect('folder_deleted')


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


for user in User.objects.all():
    UserProfile.objects.get_or_create(user=user)


def update_task_status(request, task_id, newstatus, new_position):
    task = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        # Ensure the new_position is an integer
        try:
            new_position = int(new_position)
        except ValueError:
            return HttpResponseBadRequest('Invalid position value')

        # Retrieve the Status instance based on the name
        status = Status.objects.get(name=newstatus)

        # Save the old position for comparison
        old_position = task.position
        old_status = task.status

        # Update task status and position
        task.status = status
        task.position = new_position
        task.save()

        # Moving within the same column (Up/Down)
        if old_status == status:
            if old_position < new_position:
                Task.objects.filter(status=status, position__gt=old_position, position__lte=new_position).exclude(
                    pk=task_id).update(position=F('position') - 1)
            elif old_position > new_position:
                Task.objects.filter(status=status, position__lt=old_position, position__gte=new_position).exclude(
                    pk=task_id).update(position=F('position') + 1)

        # Moving between columns
        else:
            # Update positions of tasks in the new column
            Task.objects.filter(status=status, position__gte=new_position).exclude(pk=task_id).update(
                position=F('position') + 1)

            # Adjust positions of tasks in the old column
            Task.objects.filter(status=old_status, position__gt=old_position).exclude(pk=task_id).update(
                position=F('position') - 1)

        # Return a JSON response
        return JsonResponse({'message': 'Task status and position updated successfully', 'status': newstatus,
                             'position': new_position})

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=400)

    # Handle other HTTP methods if needed


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
        print(form)
        if form.is_valid():
            project = form.save(commit=False)


            # Save the project first
            project.save()

            # Get the tag names entered by the user
            tag_names = form.cleaned_data.get('tags')

            # Split the tag names by comma and create tags
            for tag_name in tag_names.split(','):
                tag_name = tag_name.strip()  # Remove leading/trailing whitespace
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

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
        project_statuses = Status.objects.filter(project=project_id).all()
        print(project_statuses)
        print(project_id)
    else:
        tasks = Task.objects.order_by('position', 'status').all()
        project_statuses = Status.objects.all()  # Fetch all statuses

    # Group tasks by status
    task_statuses = {}
    for task in tasks:
        status_name = task.status.name
        if status_name not in task_statuses:
            task_statuses[status_name] = []
        task_statuses[status_name].append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'xp_reward': task.xp_reward,
        })

    # Include profile picture information in the context
    user_profile_picture = request.user.userprofile.profile_picture if hasattr(request.user, 'userprofile') else None
    # print(task_statuses)
    # print(project_statuses)
    return render(request, 'task_list.html', {
        'task_statuses': task_statuses,
        'form': TaskForm(),
        'tasks': tasks,
        'user_profile_picture': user_profile_picture,
        'project_statuses': project_statuses,
    })


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def change_priority(request, task_id):
    task = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        new_priority = request.POST.get('priority')
        # print(f"Received new priority: {new_priority}")  # Add this line to check if data is received correctly
        task.priority = new_priority
        task.save()
        # print("Task priority updated successfully")  # Add this line to check if the task is saved successfully

    return redirect('task_list')


def create_task(request, status_name):
    # Get the Status instance based on the provided status name
    status = get_object_or_404(Status, name=status_name)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = status

            # Get the maximum position in the current status
            max_position = Task.objects.filter(status=status).aggregate(Max('position'))['position__max']

            # Set the new task's position to one greater than the maximum position
            task.position = max_position + 1 if max_position is not None else 1

            # Save the task first to get an ID
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
