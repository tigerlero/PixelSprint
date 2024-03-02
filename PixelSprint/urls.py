from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/', include('project.urls')),  # Replace 'your_app' with your app's name

    # Add a pattern for the root path
    path('', include('project.urls')),  # Replace 'your_app' with your app's name
]
# Add these lines at the end of your urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
