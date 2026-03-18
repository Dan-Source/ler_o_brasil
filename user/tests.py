from django.contrib.auth import get_user_model
from django.test import TestCase

from user.factories import UserFactory

User = get_user_model()


class UserFactoryTests(TestCase):
    """Tests for UserFactory functionality."""

    def test_creates_valid_user(self):
        """Test that factory creates a valid user."""
        user = UserFactory.create()
        self.assertIsNotNone(user.pk)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        self.assertTrue(user.is_active)

    def test_password_is_hashed(self):
        """Test that password is properly hashed."""
        user = UserFactory.create()
        self.assertTrue(user.check_password("testpass123"))
        # Ensure password is not stored in plain text
        self.assertNotEqual(user.password, "testpass123")

    def test_staff_trait(self):
        """Test staff trait creates staff user."""
        user = UserFactory.create(staff=True)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser_trait(self):
        """Test superuser trait creates superuser."""
        user = UserFactory.create(superuser=True)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_creates_batch(self):
        """Test batch creation."""
        users = UserFactory.create_batch(5)
        self.assertEqual(len(users), 5)
        self.assertEqual(User.objects.count(), 5)

    def test_unique_usernames(self):
        """Test that usernames are unique."""
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        self.assertNotEqual(user1.username, user2.username)

    def test_custom_username(self):
        """Test creating user with custom username."""
        user = UserFactory.create(username="customuser")
        self.assertEqual(user.username, "customuser")
