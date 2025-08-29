from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Detection, UploadedVideo
from .utils import run_detection
import os
import random
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import models
import base64
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedVideo, Detection
from .utils import run_detection
import os, json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect



# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             Detection.objects.all().delete()  # Caution: deletes all detections

#             uploaded_video = form.save()
#             detections = run_detection(uploaded_video.video.path)
#             base_time = uploaded_video.uploaded_at

#             for i, det in enumerate(detections):
#                 # Optional: skip if you don’t want to store images

#                 Detection.objects.create(
#                     video=uploaded_video,
#                     image_base64=det["image_data"],
#                     detected_at=base_time + timedelta(seconds=i * 2),
#                     latitude=round(random.uniform(25.60, 25.65), 6),
#                     longitude=round(random.uniform(85.05, 85.15), 6),
#                     ward_number=random.randint(1, 49)
#                 )            
#             return redirect('dashboard')
#     else:
#         form = VideoUploadForm()
#     return render(request, 'detections/upload.html', {'form': form})
def homepage(request):
    return redirect('login')
@login_required
def dashboard(request):
    detections = Detection.objects.all().order_by( models.Case(models.When(status='pending', then=0), models.When(status='cleaned', then=1),)  ,'-detected_at')#####
    is_supervisor = request.user.groups.filter(name='supervisors').exists()

    return render(request, 'detections/dashboard.html', {'detections': detections,'is_supervisor': is_supervisor})

def map_view(request):
    pending_detections = Detection.objects.filter(status='pending')
    return render(request, 'detections/map.html', {'detections': pending_detections})

def is_supervisor(user):
    return user.groups.filter(name='supervisors').exists()



@login_required
@user_passes_test(lambda u: u.groups.filter(name='supervisors').exists())
@require_POST

def update_status(request):
    if request.method == 'POST':
        detection_id = request.POST.get('id')
        detection = get_object_or_404(Detection, id=detection_id)

        # Toggle status
        detection.status = 'cleaned' if detection.status == 'pending' else 'pending'
        detection.save()
        return JsonResponse({'status': detection.status})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AndroidUploadAPI(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('video_file')
        json_file = request.FILES.get('json_file')

        if not video_file or not json_file:
            return Response({"error": "Missing video_file or json_file"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the video
        uploaded_video = UploadedVideo.objects.create(video=video_file)

        # Save the JSON metadata
        json_path = os.path.join('media/jsons', json_file.name)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'wb+') as f:
            for chunk in json_file.chunks():
                f.write(chunk)

        with open(json_path, 'r') as f:
            metadata = json.load(f)

        location_data = metadata.get('location_data', [])
        if not location_data:
            return Response({"error": "No location data found in JSON"}, status=400)

        fps = metadata.get('fps', 30)  # fallback if not provided

        detections = run_detection(uploaded_video.video.path)

        def closest_location(rel_time_ms):
            return min(location_data, key=lambda loc: abs(loc['relative_time_ms'] - rel_time_ms))

        for det in detections:
            frame_number = det["frame_number"]
            rel_time_ms = int((frame_number / fps) * 1000)
            loc = closest_location(rel_time_ms)

            Detection.objects.create(
                video=uploaded_video,
                image_base64=det["image_data"],
                detected_at=datetime.utcfromtimestamp(loc["timestamp"] / 1000.0),
                latitude=loc["latitude"],
                longitude=loc["longitude"],
                ward_number=1  # hardcoded for now
            )

        return Response({"message": "Upload successful", "detections": len(detections)}, status=201)