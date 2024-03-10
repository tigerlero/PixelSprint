

from django.urls import path, include
from . import views
from .views import register_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('user_profile/', views.user_profile_form_view, name='user_profile_form'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('', views.homepage, name='homepage'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.create_or_update_project, name='create_project'),
    path('projects/update/<int:project_id>/', views.create_or_update_project, name='update_project'),
    path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('register/', register_view, name='register'),
    path('change_priority/<int:task_id>/', views.change_priority, name='change_priority'),
    path('tasks/<int:project_id>/', views.task_list, name='task_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('update_task_status/<int:task_id>/<str:newstatus>/<int:new_position>/', views.update_task_status, name='update_task_status'),
    path('create_task/<str:status_name>/', views.create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/update/<int:note_id>/', views.update_note, name='update_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    # Paths for space views
    path('space/create/', views.create_or_update_space, name='space_form'),
    path('space/update/<int:space_id>/', views.create_or_update_space, name='update_space'),
    path('space/', views.space_list, name='space_list'),
    path('space/<int:space_id>/', views.space_detail, name='space_detail'),
    path('space/delete/<int:space_id>/', views.delete_space, name='delete_space'),

    # Paths for folder views
    path('folder/create/', views.create_or_update_folder, name='folder_form'),
    path('folder/update/<int:folder_id>/', views.create_or_update_folder, name='update_folder'),
    path('folder/', views.folder_list, name='folder_list'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('folder/delete/<int:folder_id>/', views.delete_folder, name='delete_folder'),

    # Paths for list views
    path('list/create/', views.create_or_update_list, name='list_form'),
    path('list/update/<int:list_id>/', views.create_or_update_list, name='update_list'),
    path('list/', views.list_list, name='list_list'),
    path('list/<int:list_id>/', views.list_detail, name='list_detail'),
    path('list/delete/<int:list_id>/', views.delete_list, name='delete_list'),

    path('userprofiles/', views.userprofile_list, name='userprofile_list'),
    path('userprofiles/<int:userprofile_id>/', views.userprofile_detail, name='userprofile_detail'),
    path('userprofiles/create/', views.create_userprofile, name='create_userprofile'),
    path('userprofiles/update/<int:userprofile_id>/', views.update_userprofile, name='update_userprofile'),
    # Add more patterns as needed
]
