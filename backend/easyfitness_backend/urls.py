from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import health_check, api_info 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include API app routes
    path('health/', health_check), 
    path('info/', api_info), 
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
