from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import pytz

# Define the target time zone (e.g., GMT)
target_timezone = pytz.timezone('Etc/GMT')

def home(request):
    return HttpResponse("Welcome to the Bus Management API")

@csrf_exempt
def receive_gps_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Convert current time to target time zone
            current_time = datetime.now(pytz.utc).astimezone(target_timezone)
            data['timestamp'] = current_time.isoformat()
            print("Received GPS data:", data)
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def receive_rfid_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Convert current time to target time zone
            current_time = datetime.now(pytz.utc).astimezone(target_timezone)
            data['scan_time'] = current_time.isoformat()
            print("Received RFID data:", data)
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)