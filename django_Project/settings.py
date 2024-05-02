"""
Django settings for django_Project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
# Secret key for cryptographic signing, keep this secret in production
SECRET_KEY = 'django-insecure-gp=acq9*6-f#&_teme0=kl-u&p4d2o!*5@zrfx%6pryp$6_oco'

# Toggle debug mode - set to False in production
DEBUG = True

# Define allowed hosts for the application
ALLOWED_HOSTS = []

# APPLICATION DEFINITION
# List of applications that are enabled in this Django project
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',   # Authentication system
    'django.contrib.contenttypes',  # Content type system
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Managing static files (CSS, images)
    # Custom app 'custom_user'
    'user.apps.UserConfig',
    'album.apps.AlbumConfig',

]

# Middleware is a framework of hooks into Django's request/response processing.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Manages security aspects
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages sessions across requests
    'django.middleware.common.CommonMiddleware',  # Handles common tasks
    'django.middleware.csrf.CsrfViewMiddleware',  # Cross-Site Request Forgery protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Associates users with requests
    'django.contrib.messages.middleware.MessageMiddleware',  # Manages temporary messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# URL Configuration: The module that Django should use for URL resolution
ROOT_URLCONF = 'django_Project.urls'

AUTHENTICATION_BACKENDS = [
    'custom_user.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

# TEMPLATES CONFIGURATION
# Settings for template processing, defining how templates are loaded and rendered
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Using Django's template engine
        'DIRS': [BASE_DIR / 'templates'],  # Custom templates directory
        'APP_DIRS': True,  # Allow app-specific template directories
        'OPTIONS': {
            # Context processors define a set of variables that will be available in all templates
            'context_processors': [
                'django.template.context_processors.debug',  # Context processor for debug mode
                'django.template.context_processors.request',  # Adds 'request' to template context
                'django.contrib.auth.context_processors.auth',  # Adds 'user' and 'perms' to context
                'django.contrib.messages.context_processors.messages',  # Enables messages framework
            ],
        },
    },
]

# WSGI APPLICATION
# Entry-point for WSGI-compatible web servers to serve your project
WSGI_APPLICATION = 'django_Project.wsgi.application'

# DATABASE CONFIGURATION
# Defines the database engine and connection parameters
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Using PostgreSQL database
        'NAME': 'project2',  # Database name
        'USER': 'postgres',  # Database user
        'PASSWORD': 'izahaha#567',  # Database password
        'HOST': 'localhost',  # Database host
        'PORT': '5432',  # Database port
    }
}

# PASSWORD VALIDATION
# Configuration for validating user passwords
AUTH_PASSWORD_VALIDATORS = [
    # Validators for password strength and similarities
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

# INTERNATIONALIZATION
# Configures language code and time zone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES CONFIGURATION
# Defines URL and directories for serving static files
STATIC_URL = 'static/'

# DEFAULT PRIMARY KEY FIELD TYPE
# Default auto-field type to use for primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#LOGIN_REDIRECT_URL = 'welcome'