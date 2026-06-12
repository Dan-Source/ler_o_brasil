import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


User = get_user_model()


class Command(BaseCommand):
    help = "Create the default admin user if it does not already exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", default=None)
        parser.add_argument("--email", default=None)
        parser.add_argument("--password", default=None)
        parser.add_argument("--country", default=None)

    def _resolve_value(self, option_value, env_name, default_value):
        if option_value:
            return option_value

        env_value = os.getenv(env_name)
        if env_value:
            return env_value

        if settings.DEBUG:
            return default_value

        raise CommandError(f"{env_name} must be set when DEBUG is False")

    def handle(self, *args, **options):
        username = self._resolve_value(
            options["username"],
            "DJANGO_DEFAULT_ADMIN_USERNAME",
            "admin",
        )
        email = self._resolve_value(
            options["email"],
            "DJANGO_DEFAULT_ADMIN_EMAIL",
            "admin@example.com",
        )
        password = self._resolve_value(
            options["password"],
            "DJANGO_DEFAULT_ADMIN_PASSWORD",
            "testpass123",
        )
        country = self._resolve_value(
            options["country"],
            "DJANGO_DEFAULT_ADMIN_COUNTRY",
            "Brasil",
        )

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "country": country,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if not created:
            self.stdout.write(
                self.style.WARNING(
                    f"Default admin '{username}' already exists. Skipping."
                )
            )
            return

        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created default admin '{username}' ({email})"
            )
        )
