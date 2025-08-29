from django.contrib import admin
from .models import UploadedVideo, Detection

admin.site.register(UploadedVideo)
admin.site.register(Detection)
