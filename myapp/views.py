from .models import HistoryLocationTracking, LatestLocationTracking, HistoryCardReaderTracking, LastProcessedRFID
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
import logging
import json
import math

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to the Bus Management API")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@csrf_exempt
def receive_gps_data(request):
    if request.method == 'POST':
        try:
            raw_data = request.body.decode('utf-8')
            logger.info(f"Received raw GPS data: {raw_data}")

            data_parts = raw_data.split(';', 1)
            if len(data_parts) != 2:
                logger.error("Invalid data format")
                return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

            device_id = data_parts[0]
            gps_data = data_parts[1]

            if gps_data.startswith("+CGPSINFO:"):
                values = gps_data.split(":")[1].strip().split(',')
                if len(values) >= 9 and all(values[:4]):
                    latitude = values[0]
                    latitude_direction = values[1]
                    longitude = values[2]
                    longitude_direction = values[3]
                    speed = values[7]
                    lat = round(convert_to_decimal_gps(latitude, latitude_direction), 6)
                    lon = round(convert_to_decimal_gps(longitude, longitude_direction), 6)

                    if not speed:
                        logger.warning("Speed is empty, data not saved")
                        return JsonResponse({'status': 'error', 'message': 'Speed is empty'}, status=400)

                    current_time_gmt7 = timezone.make_aware(datetime.utcnow() + timedelta(hours=7))

                    last_location = LatestLocationTracking.objects.filter(device_id=device_id).first()
                    if last_location:
                        last_lat, last_lon = map(float, last_location.location.split(','))
                        distance = haversine(last_lat, last_lon, lat, lon)
                        if distance < 0.005:
                            logger.info(f"Skipping insertion for device_id: {device_id} as the location has not changed significantly")
                            return JsonResponse({'status': 'success', 'message': 'Location has not changed significantly'}, status=200)

                    history_gps_data = HistoryLocationTracking(
                        device_id=device_id,
                        location=f"{lat},{lon}",
                        speed=speed,
                        timestamp=current_time_gmt7
                    )
                    history_gps_data.save()

                    LatestLocationTracking.objects.update_or_create(
                        device_id=device_id,
                        defaults={
                            'location': f"{lat},{lon}",
                            'speed': speed,
                            'timestamp': current_time_gmt7
                        }
                    )
                    logger.info("GPS data saved successfully")
                    return JsonResponse({'status': 'success', 'data': raw_data}, status=200)
                else:
                    logger.error("Incomplete GPS data")
                    return JsonResponse({'status': 'error', 'message': 'Incomplete GPS data'}, status=400)
            logger.error("Invalid GPS data format")
            return JsonResponse({'status': 'error', 'message': 'Invalid GPS data format'}, status=400)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def convert_to_decimal_gps(value, direction):
    try:
        degrees = int(float(value) / 100)
        minutes = float(value) - (degrees * 100)
        decimal = degrees + minutes / 60.0
        if direction in ["S", "W"]:
            decimal = -decimal
        return decimal
    except ValueError:
        logger.error(f"Invalid GPS value: {value}")
        return None

@csrf_exempt
def receive_rfid_data(request):
    if request.method == 'POST':
        try:
            raw_data = request.body.decode('utf-8')
            logger.info(f"Received raw RFID data: {raw_data}")

            data = json.loads(raw_data)
            if isinstance(data, list):
                for item in data:
                    device_id, uid = item.split(',')
                    reversed_uid = reverse_uid(uid)
                    decimal_uid = convert_to_decimal(reversed_uid)

                    # Get current UTC time
                    current_time_utc = datetime.utcnow()
                    # Convert to GMT+7
                    current_time_gmt7 = current_time_utc + timedelta(hours=7)

                    # Convert naive datetime to aware datetime
                    current_time_gmt7 = timezone.make_aware(current_time_gmt7, timezone.get_current_timezone())

                    # Save to HistoryCardReaderTracking
                    rfid_data = HistoryCardReaderTracking(
                        device_id=device_id,
                        UID=decimal_uid,
                        scan_time=current_time_gmt7
                    )
                    rfid_data.save()

                    # Check if the device_id exists in LastProcessedRFID
                    last_processed_rfid, created = LastProcessedRFID.objects.get_or_create(
                        device_id=device_id
                    )
                    if created:
                        logger.info(f"Initialized LastProcessedRFID for device_id: {device_id}")

                logger.info("RFID data saved successfully")
                return JsonResponse({'status': 'success', 'data': raw_data}, status=200)
            else:
                logger.error("Invalid JSON format: Expected a list")
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format: Expected a list'}, status=400)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def update_last_processed_rfid(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Updating LastProcessedRFID: {data}")

            # Update the last processed RFID data
            LastProcessedRFID.objects.update_or_create(
                device_id=data['device_id'],
                defaults={'last_scan_time': data['last_scan_time']}
            )
            logger.info("LastProcessedRFID updated successfully")
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_gps_data(request):
    if request.method == 'GET':
        gps_data = list(HistoryLocationTracking.objects.all().values())
        return JsonResponse({'status': 'success', 'data': gps_data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_last_gps_data(request):
    if request.method == 'GET':
        gps_data = list(LatestLocationTracking.objects.all().values())
        return JsonResponse({'status': 'success', 'data': gps_data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_last_rfid_data(request):
    if request.method == 'GET':
        last_processed_timestamps = LastProcessedRFID.objects.all()
        response_data = []
        for record in last_processed_timestamps:
            device_id = record.device_id
            last_timestamp = record.last_scan_time
            new_rfid_data = HistoryCardReaderTracking.objects.filter(device_id=device_id, scan_time__gt=last_timestamp)
            response_data.extend(new_rfid_data.values())
        return JsonResponse({'status': 'success', 'data': response_data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def reverse_uid(uid):
    reversed_uid = ''.join([uid[i:i+2] for i in range(0, len(uid), 2)][::-1])
    return reversed_uid

def convert_to_decimal(reversed_uid):
    decimal_uid = int(reversed_uid, 16)
    return decimal_uid

def convert_to_decimal_gps(value, direction):
    degrees = int(float(value) / 100)
    minutes = float(value) - (degrees * 100)
    decimal = degrees + minutes / 60.0
    if direction in ["S", "W"]:
        decimal = -decimal
    return decimal