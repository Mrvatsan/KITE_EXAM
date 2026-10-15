"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
import os

def home(request):
    """
    Healthcheck endpoint for deployment monitors and root redirect to frontend.
    """
    if 'text/html' not in request.headers.get('accept', ''):
        return JsonResponse({
            'status': 'online',
            'service': 'KGiSL Exam Portal Backend API',
            'version': '1.0'
        })
    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000').rstrip('/')
    return redirect(f"{frontend_url}/admin/dashboard")

def health_check(request):
    """Explicit healthcheck endpoint for Render and uptime monitoring."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'KGiSL Exam Portal Backend',
        'timestamp': os.environ.get('RENDER_INSTANCE_ID', 'local')
    })

urlpatterns = [
    path('', home, name='home'),
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.exams.urls')),
    path('api/faculty/', include('apps.faculty.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
