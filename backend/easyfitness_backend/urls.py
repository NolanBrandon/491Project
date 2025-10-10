from django.contrib import admin
from django.urls import path, include
from api.views import health_check, api_info

urlpatterns = [
    path('admin/', admin.site.urls),          # Optional if you use admin
    path('health/', health_check, name='health_check'),
    path('info/', api_info, name='api_info'),
    path('api/', include('api.urls')),        # include all other API routes
]
