import os
import sys

# Add your project directory to the sys.path
sys.path.append('/home/diennd25/test-bus-api')

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Activate your virtual environment
activate_this = '/home/diennd25/myenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()