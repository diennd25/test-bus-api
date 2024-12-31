from django.db import models

class BusCardReaderHistory(models.Model):
    device_id = models.IntegerField()
    scan_time = models.DateTimeField()
    UID = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.device_id} - {self.UID}"