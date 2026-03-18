import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from home.models import Category


class CategoryFactory(DjangoModelFactory):
    """Factory for creating Category instances."""

    class Meta:
        model = Category
        django_get_or_create = ("slug",)

    name = factory.Faker("word", locale="pt_BR")

    @factory.lazy_attribute
    def slug(self):
        """Generate unique slug by appending sequence number if needed."""
        base_slug = slugify(self.name)
        # Check if slug exists and add sequence number if needed
        if Category.objects.filter(slug=base_slug).exists():
            sequence = Category.objects.filter(slug__startswith=base_slug).count()
            return f"{base_slug}-{sequence}"
        return base_slug
