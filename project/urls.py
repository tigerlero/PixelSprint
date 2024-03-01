

from django.urls import path
from . import views
from .views import register_view
from django.contrib.auth import views as auth_views
from .views import login_view

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', login_view, name='login'),
    path('', views.homepage, name='homepage'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.create_or_update_project, name='create_project'),
    path('projects/update/<int:project_id>/', views.create_or_update_project, name='update_project'),
    path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('register/', register_view, name='register'),
    path('change_priority/<int:task_id>/', views.change_priority, name='change_priority'),
    path('tasks/', views.task_list, name='task_list'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('update_task_status/<int:task_id>/<str:new_status>/<int:new_position>/', views.update_task_status, name='update_task_status'),
    path('create_task/<str:status>/', views.create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('notes/', views.note_list, name='note_list'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/update/<int:note_id>/', views.update_note, name='update_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),

    path('userprofiles/', views.userprofile_list, name='userprofile_list'),
    path('userprofiles/<int:userprofile_id>/', views.userprofile_detail, name='userprofile_detail'),
    path('userprofiles/create/', views.create_userprofile, name='create_userprofile'),
    path('userprofiles/update/<int:userprofile_id>/', views.update_userprofile, name='update_userprofile'),
    # Add more patterns as needed
]
