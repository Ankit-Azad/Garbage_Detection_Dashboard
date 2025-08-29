"""
URL configuration for garbage_dashboard project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # ✅ Add this
from detections import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # ✅ Login route
    # path('login/', auth_views.LoginView.as_view(template_name='detections/login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map_view, name='map'),
    path('api/update-status/', views.update_status, name='update_status'),
    # path('api/upload/', views.android_upload, name='android_upload'),
    path('api/upload/', views.AndroidUploadAPI.as_view(), name='android_upload')

    
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
