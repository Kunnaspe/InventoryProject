import os
from pathlib import Path

# Sets up the base directory for my project
BASE_DIR = Path(__file__).resolve().parent.parent


# Configures settings for my dev env

# This is a secret for a reason
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-placeholder-change-in-production')

# Turn off DEBUG in prod
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Allows localhost  for dev, configure environment variables for prod
allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host.strip()]


# Key apps

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
]

# middleware that handles security, sessions, and other important functions
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
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


# Project settings

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# URL for my static CSS and JavaScript files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
