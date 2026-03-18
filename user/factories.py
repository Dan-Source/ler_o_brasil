import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker("first_name", locale="pt_BR")
    last_name = factory.Faker("last_name", locale="pt_BR")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    country = factory.Faker("country", locale="pt_BR")
    is_active = True
    is_staff = False
    is_superuser = False
    password = factory.PostGenerationMethodCall("set_password", "testpass123")

    class Params:
        staff = factory.Trait(
            is_staff=True,
        )
        superuser = factory.Trait(
            is_staff=True,
            is_superuser=True,
        )
