from django.db import models
from django.utils import timezone

class HistoryLocationTracking(models.Model):
    device_id = models.IntegerField()
    location = models.CharField(max_length=255)
    speed = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

class LatestLocationTracking(models.Model):
    device_id = models.IntegerField(unique=True)
    location = models.CharField(max_length=255)
    speed = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

class HistoryCardReaderTracking(models.Model):
    device_id = models.IntegerField()
    UID = models.CharField(max_length=50)
    scan_time = models.DateTimeField(default=timezone.now)

class LastProcessedRFID(models.Model):
    device_id = models.IntegerField(unique=True)
    last_scan_time = models.DateTimeField(default=timezone.now)