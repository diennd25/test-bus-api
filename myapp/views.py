from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from datetime import datetime

def home(request):
    return HttpResponse("Welcome to the Bus Management API")

@csrf_exempt
def test_post_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')
            timestamp = data.get('scan_time')
            UID = data.get('UID')

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO bus_card_reader_history (device_id, scan_time, UID) VALUES (%s, %s, %s)",
                    [device_id, timestamp, UID]
                )

            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)