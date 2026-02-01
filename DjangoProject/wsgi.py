# Sets up the WSGI

import os

from django.core.wsgi import get_wsgi_application

# Default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

application = get_wsgi_application()
