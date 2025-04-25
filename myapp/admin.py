from django.contrib import admin
from .models import HistoryLocationTracking, LatestLocationTracking, HistoryCardReaderTracking

admin.site.register(HistoryLocationTracking)
admin.site.register(LatestLocationTracking)
admin.site.register(HistoryCardReaderTracking)