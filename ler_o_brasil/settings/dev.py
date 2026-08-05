import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-i#81c2yqf^^knez7$j_8#*d00@vew9iaxvek+_39bu(^i-ppd9",
)

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS
CORS_ALLOWED_ORIGINS = os.getenv("DJANGO_CORS_ALLOWED_ORIGINS", "http://localhost:8080").split(",")

CORS_ALLOW_CREDENTIALS = os.getenv("DJANGO_CORS_ALLOW_CREDENTIALS", "true").lower() in (
    "true",
    "1",
    "t",
)

CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "http://localhost:8080").split(",")

try:
    from .local import *
except ImportError:
    pass
