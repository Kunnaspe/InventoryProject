from django.shortcuts import render
from .models import Product

# Retrieves and displays all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

# Enables product search
def product_search(request):
    query = request.GET.get('q')
    if query:
        # filters products
        products = Product.objects.filter(ProductNumber__icontains=query)
    else:
        # returns empty list if appropriate
        products = Product.objects.none()
    return render(request, 'inventory/product_search.html', {'products': products, 'query': query})
