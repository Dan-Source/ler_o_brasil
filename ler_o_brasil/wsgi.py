"""
WSGI config for ler_o_brasil project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get("ENVIRONMENT", "dev")
settings_module = f"ler_o_brasil.settings.{environment}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
