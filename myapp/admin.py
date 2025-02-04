from django.contrib import admin
from .models import GPSData, RFIDData

admin.site.register(GPSData)
admin.site.register(RFIDData)