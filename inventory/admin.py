from django.contrib import admin
from .models import Product, Department

# Listing the models that I need to manage in the Django admin interface
admin.site.register(Product)
admin.site.register(Department)
