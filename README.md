# Garbage Detection & Monitoring Dashboard (Django)

This repository contains the **Django-based backend and dashboard** for an AI-powered urban sanitation monitoring system. The dashboard visualizes garbage detection results generated from geo-tagged video data and supports data-driven decision-making for municipal sanitation planning.

---

## Project Overview

The system automates garbage hotspot detection by integrating:
- a **mobile data collection app** for geo-tagged video capture, and
- an **AI inference pipeline** for garbage detection.

This repository focuses on the **server-side ingestion, AI integration, storage, and visualization layer**.

---

## System Workflow

1. Android mobile app captures video with real-time GPS (latitude, longitude) and timestamp.
2. Metadata is formatted as structured **JSON** and sent to the Django backend.
3. Backend forwards video data to a trained **YOLOv8** model for inference.
4. Detected garbage instances are stored in the database.
5. Results are displayed on a **web-based dashboard** for monitoring and planning.

---

## Key Features

- REST-based ingestion of geo-tagged video metadata  
- Integration with YOLOv8 garbage detection model  
- Storage of detection results for analysis  
- Dashboard view for garbage hotspots and detection logs  
- Designed for municipal-scale sanitation monitoring

---

## Tech Stack

- Backend: Django, Django REST Framework  
- Database: PostgreSQL  
- AI Model: YOLOv8  
- Frontend: Django Templates  
- Data Format: JSON (GPS, timestamp, detection metadata)

---
### Clone the Repository
```bash
git clone https://github.com/Ankit-Azad/Garbage_Detection_Dashboard.git
cd Garbage_Detection_Dashboard
