from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/', include('project.urls')),  # Replace 'your_app' with your app's name

    # Add a pattern for the root path
    path('', include('project.urls')),  # Replace 'your_app' with your app's name
]