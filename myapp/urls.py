from django.urls import path
from .views import receive_gps_data, receive_rfid_data, get_gps_data, get_last_gps_data, get_last_rfid_data, update_last_processed_rfid, health_check

urlpatterns = [
    path('receive-gps/', receive_gps_data, name='receive_gps_data'),
    path('receive-rfid/', receive_rfid_data, name='receive_rfid_data'),
    path('get-gps/', get_gps_data, name='get_gps_data'),
    path('get-last-gps/', get_last_gps_data, name='get_last_gps_data'),
    path('get-last-rfid/', get_last_rfid_data, name='get_last_rfid_data'),
    path('update-last-processed-rfid/', update_last_processed_rfid, name='update_last_processed_rfid'),
    path('health/', health_check, name='health_check'),
]
