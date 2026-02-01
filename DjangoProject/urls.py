# URL routing for DjangoProject
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Path to the Django admin site
    path('admin/', admin.site.urls),
    # URL path for the inventory app
    path('inventory/', include('inventory.urls')),
]
