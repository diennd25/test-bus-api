import os
import sys

# Add your project directory to the sys.path
sys.path.append('/root/Downloads/test-bus-api')  # Update this to match your actual path

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
