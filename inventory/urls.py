from django.urls import path
from . import views

# Traffic routing urls
urlpatterns = [
    # Provides our list view
    path('', views.product_list, name='product_list'),
    # Connects the search
    path('search/', views.product_search, name='product_search'),
]
