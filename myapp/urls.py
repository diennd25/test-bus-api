from django.urls import path
from .views import receive_gps_data, receive_rfid_data, get_gps_data, get_rfid_data

urlpatterns = [
    path('receive-gps/', receive_gps_data, name='receive_gps_data'),
    path('receive-rfid/', receive_rfid_data, name='receive_rfid_data'),
    path('get-gps/', get_gps_data, name='get_gps_data'),
    path('get-rfid/', get_rfid_data, name='get_rfid_data'),
]