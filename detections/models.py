from django.db import models

class UploadedVideo(models.Model):
    video = models.FileField(upload_to='detections/videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} uploaded at {self.uploaded_at}"

class Detection(models.Model):
    video = models.ForeignKey('UploadedVideo', on_delete=models.CASCADE)
    # Remove the file path field:
    # image = models.ImageField(upload_to='detections/outputs/')
    # Add a base64 field instead:
    image_base64 = models.TextField(blank=True)  # holds encoded image

    detected_at = models.DateTimeField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    ward_number = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('cleaned', 'Cleaned')],
        default='pending'
    )

    def __str__(self):
        return f"Detection on video {self.video.id} at {self.detected_at}"