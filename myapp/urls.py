from django.urls import path
from .views import receive_gps_data, receive_rfid_data

urlpatterns are [
    path('receive-gps/', receive_gps_data, name='receive_gps_data'),
    path('receive-rfid/', receive_rfid_data, name='receive_rfid_data'),
]