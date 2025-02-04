# models.py

from django.db import models
from django.utils import timezone

class GPSData(models.Model):
    device_id = models.IntegerField()
    location = models.CharField(max_length=255)
    speed = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

class RFIDData(models.Model):
    device_id = models.IntegerField()
    UID = models.CharField(max_length=50)
    scan_time = models.DateTimeField(default=timezone.now)