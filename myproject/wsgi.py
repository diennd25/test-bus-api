import os
import sys

# Add your project directory to the sys.path
sys.path.append('/home/diennd25/test-bus-api')
sys.path.append('/home/diennd25/test-bus-api/myproject')

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Activate your virtual environment
virtualenv = '/home/diennd25/myenv'
os.environ['VIRTUAL_ENV'] = virtualenv
os.environ['PATH'] = f"{virtualenv}/bin:{os.environ['PATH']}"
sys.path.append(f"{virtualenv}/lib/python3.10/site-packages")

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()