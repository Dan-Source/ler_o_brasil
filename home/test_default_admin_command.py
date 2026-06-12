import os
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from user.models import User


class CreateDefaultAdminCommandTests(TestCase):
    def test_creates_default_admin_from_env(self):
        with patch.dict(
            os.environ,
            {
                "DJANGO_DEFAULT_ADMIN_USERNAME": "siteadmin",
                "DJANGO_DEFAULT_ADMIN_EMAIL": "siteadmin@example.com",
                "DJANGO_DEFAULT_ADMIN_PASSWORD": "super-secret",
                "DJANGO_DEFAULT_ADMIN_COUNTRY": "Brasil",
            },
            clear=False,
        ):
            call_command("create_default_admin")

        user = User.objects.get(username="siteadmin")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, "siteadmin@example.com")
        self.assertEqual(user.country, "Brasil")
        self.assertTrue(user.check_password("super-secret"))

    def test_skips_existing_admin(self):
        existing_user = User.objects.create_user(
            username="admin",
            email="existing@example.com",
            password="original-secret",
            country="Brasil",
        )

        with patch.dict(
            os.environ,
            {
                "DJANGO_DEFAULT_ADMIN_USERNAME": "admin",
                "DJANGO_DEFAULT_ADMIN_EMAIL": "new@example.com",
                "DJANGO_DEFAULT_ADMIN_PASSWORD": "new-secret",
                "DJANGO_DEFAULT_ADMIN_COUNTRY": "Portugal",
            },
            clear=False,
        ):
            call_command("create_default_admin")

        existing_user.refresh_from_db()

        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(existing_user.is_staff)
        self.assertFalse(existing_user.is_superuser)
        self.assertEqual(existing_user.email, "existing@example.com")
        self.assertEqual(existing_user.country, "Brasil")
        self.assertTrue(existing_user.check_password("original-secret"))

    @override_settings(DEBUG=False)
    def test_requires_env_vars_when_debug_is_false(self):
        with patch.dict(
            os.environ,
            {
                "DJANGO_DEFAULT_ADMIN_USERNAME": "",
                "DJANGO_DEFAULT_ADMIN_EMAIL": "",
                "DJANGO_DEFAULT_ADMIN_PASSWORD": "",
                "DJANGO_DEFAULT_ADMIN_COUNTRY": "",
            },
            clear=False,
        ):
            with self.assertRaises(CommandError):
                call_command("create_default_admin")
