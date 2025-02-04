from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from .models import GPSData, RFIDData

def home(request):
    return HttpResponse("Welcome to the Bus Management API")

@csrf_exempt
def receive_gps_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gps_data = GPSData(
                device_id=data['device_id'],
                location=data['location'],
                speed=data['speed']
            )
            gps_data.save()
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def receive_rfid_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rfid_data = RFIDData(
                device_id=data['device_id'],
                UID=data['UID']
            )
            rfid_data.save()
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)