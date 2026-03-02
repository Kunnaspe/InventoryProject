from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product


# @login_required redirects unauthenticated requests to LOGIN_URL (/accounts/login/)
# before allowing access to any inventory page.

@login_required
def product_list(request):
    # Retrieves and displays all products
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


@login_required
def product_search(request):
    # Enables product search by product number
    query = request.GET.get('q')
    if query:
        # Filters products whose ProductNumber contains the query string (case-insensitive)
        products = Product.objects.filter(ProductNumber__icontains=query)
    else:
        # Returns an empty queryset when no search term is provided
        products = Product.objects.none()
    return render(request, 'inventory/product_search.html', {'products': products, 'query': query})
