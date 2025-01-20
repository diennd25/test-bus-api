from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

def home(request):
    return HttpResponse("Welcome to the Bus Management API")

@csrf_exempt
def receive_gps_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data['timestamp'] = datetime.now().isoformat()
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
            data['scan_time'] = datetime.now().isoformat()
            print("Received RFID data:", data)
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)