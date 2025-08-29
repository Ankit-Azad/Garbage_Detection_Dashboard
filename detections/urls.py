from django.urls import path
from . import views
from .views import AndroidUploadAPI


urlpatterns = [
    # path('', views.upload_video, name='upload'),           # Home page
    path('dashboard/', views.dashboard, name='dashboard'), # Detection dashboard
    path('map/', views.map_view, name='map'),              # Map view
    path('api/update-status/', views.update_status, name='update_status'),  # Optional
    path('api/upload/', AndroidUploadAPI.as_view(), name='android_upload'),

]
