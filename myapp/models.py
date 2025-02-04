from django.db import models

class GPSData(models.Model):
    device_id = models.IntegerField()
    location = models.CharField(max_length=255)
    speed = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class RFIDData(models.Model):
    device_id = models.IntegerField()
    UID = models.CharField(max_length=50)
    scan_time = models.DateTimeField(auto_now_add=True)