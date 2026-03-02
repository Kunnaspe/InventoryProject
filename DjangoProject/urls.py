# URL routing for DjangoProject
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Path to the Django admin site
    path('admin/', admin.site.urls),
    # Cognito's new console only accepts simple callback paths, so we register
    # /callback in Cognito and redirect here to the real allauth handler.
    path('callback', RedirectView.as_view(url='/accounts/oidc/cognito/login/callback/', query_string=True)),
    # django-allauth handles all OAuth/OIDC flows under /accounts/
    # This includes the Cognito OIDC callback:
    #   /accounts/oidc/cognito/login/callback/
    # as well as the login and logout pages:
    #   /accounts/login/
    #   /accounts/logout/
    path('accounts/', include('allauth.urls')),
    # URL path for the inventory app (protected by @login_required)
    path('inventory/', include('inventory.urls')),
]
