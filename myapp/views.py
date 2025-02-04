from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from .models import GPSData, RFIDData
import logging

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to the Bus Management API")

@csrf_exempt
def receive_gps_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received GPS data: {data}")
            gps_data = GPSData(
                device_id=data['device_id'],
                location=data['location'],
                speed=data['speed']
            )
            gps_data.save()
            logger.info("GPS data saved successfully")
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def receive_rfid_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received RFID data: {data}")
            rfid_data = RFIDData(
                device_id=data['device_id'],
                UID=data['UID']
            )
            rfid_data.save()
            logger.info("RFID data saved successfully")
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_gps_data(request):
    if request.method == 'GET':
        gps_data = list(GPSData.objects.all().values())
        return JsonResponse({'status': 'success', 'data': gps_data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_rfid_data(request):
    if request.method == 'GET':
        rfid_data = list(RFIDData.objects.all().values())
        return JsonResponse({'status': 'success', 'data': rfid_data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)