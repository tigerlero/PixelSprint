from django.contrib import admin
from .models import UserProfile, Project, Task, Note

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Note)