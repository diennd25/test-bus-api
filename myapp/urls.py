from django.urls import path
from .views import test_post_data

urlpatterns = [
    path('test-post/', test_post_data, name='test_post_data'),
]