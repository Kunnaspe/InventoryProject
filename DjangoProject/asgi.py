# ASGI callable as a module-level variable

import os

from django.core.asgi import get_asgi_application

# Default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

application = get_asgi_application()
