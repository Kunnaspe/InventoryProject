import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Sets up the base directory for my project
BASE_DIR = Path(__file__).resolve().parent.parent


# Configures settings for my dev env

# This is a secret for a reason
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-placeholder-change-in-production')

# Turn off DEBUG in prod
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Allows localhost for dev, configure environment variables for prod
allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host.strip()]

# Required for CSRF protection when requests arrive via CloudFront (HTTPS)
csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins.split(',') if o.strip()]


# Key apps — includes Django built-ins, allauth for OAuth/OIDC, and the inventory app

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Required by django-allauth: provides Site model for multi-site support
    'django.contrib.sites',
    # Core allauth package
    'allauth',
    # Allauth account management (login/logout/session flow)
    'allauth.account',
    # Allauth social/OAuth/OIDC account support
    'allauth.socialaccount',
    # Generic OpenID Connect provider — used to integrate AWS Cognito as an OIDC IdP
    'allauth.socialaccount.providers.openid_connect',
    # Our inventory application
    'inventory',
]

# Middleware that handles security, sessions, and other important functions.
# AccountMiddleware is required by django-allauth (0.56+) for request-scoped auth state.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Required by django-allauth: manages allauth-specific per-request context
    'allauth.account.middleware.AccountMiddleware',
]

# Project URL
ROOT_URLCONF = 'DjangoProject.urls'

# Config template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Identify the WSGI app
WSGI_APPLICATION = 'DjangoProject.wsgi.application'


# Use MariaDB in prod, SQLite in local dev
db_host = os.environ.get('DB_HOST', '')
if db_host:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': db_host,
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'ssl': {'ca': os.environ.get('DB_SSL_CA', '')} if os.environ.get('DB_SSL_CA') else {},
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Standard password validators for account security

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Authentication backends
# ModelBackend: handles Django admin login and any local username/password auth
# AuthenticationBackend: required by allauth to authenticate users returned from Cognito

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# django.contrib.sites: SITE_ID=1 matches the default "example.com" site entry.
# django-allauth requires this to associate OAuth apps with the current site.

SITE_ID = 1


# Redirect behaviour
# Unauthenticated requests to @login_required views are sent here first
LOGIN_URL = '/accounts/login/'
# After a successful Cognito login, land on the inventory list
LOGIN_REDIRECT_URL = '/inventory/'
# After logout, return to the login page
LOGOUT_REDIRECT_URL = '/accounts/login/'


# django-allauth account settings

# Skip local email-verification — Cognito handles its own user verification
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Email is collected from the Cognito ID token claims
ACCOUNT_EMAIL_REQUIRED = True
# Do not require a username — use email as the primary identifier
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# Automatically create a Django user record on the first Cognito login
SOCIALACCOUNT_AUTO_SIGNUP = True


# AWS Cognito OIDC provider configuration
# AWS Cognito exposes a standard OpenID Connect discovery endpoint at:
#  https://cognito-idp.<region>.amazonaws.com/<user_pool_id>/.well-known/openid-configuration
# Steps I used to set up Cognito:
#   1. In the AWS Console, Cognito > User Pools > Create user pool
#   2. Under App Integration > App clients, add a new public client
#   3. Set callback URL to:
#   4. Enable the Authorization code grant OAuth flow
#   5. Enable the openid, email, and profile OAuth scopes
#   6. Note User Pool ID (format: <region>_XXXXXXXXX) and App Client ID/Secret
#   7. Set the environment variables below in .env file

SOCIALACCOUNT_PROVIDERS = {
    'openid_connect': {
        'APPS': [
            {
                # provider_id becomes part of the callback URL:
                # /accounts/oidc/cognito/login/callback/
                'provider_id': 'cognito',
                'name': 'AWS Cognito',
                # App Client ID from the Cognito User Pool App Client settings
                'client_id': os.environ.get('COGNITO_CLIENT_ID', ''),
                # App Client Secret from the Cognito User Pool App Client settings
                'secret': os.environ.get('COGNITO_CLIENT_SECRET', ''),
                'settings': {
                    # OIDC issuer URL — allauth appends /.well-known/openid-configuration
                    # Format: https://cognito-idp.<region>.amazonaws.com/<user_pool_id>
                    'server_url': os.environ.get('COGNITO_SERVER_URL', ''),
                },
            }
        ]
    }
}


# Project settings

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# URL for static CSS and JavaScript files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
