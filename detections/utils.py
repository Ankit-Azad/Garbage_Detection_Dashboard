import base64
import cv2
from io import BytesIO
from ultralytics import YOLO
from pathlib import Path
import numpy as np
import os
from django.conf import settings
import json
from datetime import datetime






MODEL_PATH = Path('model/best1.pt')

def run_detection(video_path):
    model = YOLO(str(MODEL_PATH))  # Load only when needed
    cap = cv2.VideoCapture(str(video_path))
    frame_num = 0
    detections = []



    mask_path = os.path.join(settings.BASE_DIR, 'detections', 'static', 'detections', 'mask1.png')
    mask = cv2.imread(mask_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

        masked_frame = cv2.bitwise_and(frame, resized_mask)

        results = model(masked_frame)

        # results = model(frame)        #

        if len(results[0].boxes) > 0:

            annotated = results[0].plot()  
            annotated_on_raw = frame.copy()
            annotated_on_raw = results[0].plot(img=annotated_on_raw)  # Re-draw on raw

            # frame_file = os.path.join(output_dir, f"frame_{frame_num}.jpg")
            # cv2.imwrite(frame_file, annotated_on_raw)


            # saved_frames.append(Path(frame_file))

            _, buffer = cv2.imencode('.jpg', annotated_on_raw)
            encoded_img = base64.b64encode(buffer).decode('utf-8')  # For optional use

            detections.append({
                "frame_number": frame_num,
                "image_data": encoded_img,
                "has_detection": True
            })




            for _ in range(30):
                cap.read()
            frame_num += 31
        else:

            frame_num += 1

    cap.release()
    return detections
