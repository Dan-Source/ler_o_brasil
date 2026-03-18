import random

import factory
import wagtail_factories
from wagtail.models import Page

from home.models import EventIndexPage, EventPage
from user.factories import UserFactory


class EventIndexPageFactory(wagtail_factories.PageFactory):
    """Factory for creating EventIndexPage instances."""

    class Meta:
        model = EventIndexPage
        django_get_or_create = ("slug",)

    title = "Eventos"
    slug = "eventos"
    description = factory.Faker("paragraph", locale="pt_BR")
    owner = factory.SubFactory(UserFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override create to handle Wagtail Page tree structure."""
        # Check if EventIndexPage already exists
        existing = EventIndexPage.objects.first()
        if existing:
            return existing

        # Get or create parent (root page)
        parent = kwargs.pop("parent", None)
        if parent is None:
            parent = Page.objects.filter(depth=2).first()
            if parent is None:
                parent = Page.get_first_root_node()

        # Create the page instance
        instance = model_class(*args, **kwargs)
        parent.add_child(instance=instance)

        return instance


class EventPageFactory(wagtail_factories.PageFactory):
    """Factory for creating EventPage instances."""

    class Meta:
        model = EventPage

    title = factory.Faker("sentence", nb_words=5, locale="pt_BR")
    description = factory.Faker("text", max_nb_chars=1000, locale="pt_BR")
    event_date = factory.Faker("future_date", end_date="+60d")
    event_time = factory.Faker("time")
    event_link = factory.Faker("url")
    owner = factory.SubFactory(UserFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override create to handle Wagtail Page tree structure."""
        # Get or create parent (must be EventIndexPage)
        parent = kwargs.pop("parent", None)
        if parent is None:
            parent = EventIndexPageFactory.create()

        # Create the page instance
        instance = model_class(*args, **kwargs)
        parent.add_child(instance=instance)

        return instance

    @factory.post_generation
    def books(obj, create, extracted, **kwargs):
        """Add books to the event after creation."""
        if not create:
            return

        if extracted:
            # If a list of books was passed, use it
            for book in extracted:
                obj.books.add(book)
        else:
            # Otherwise, create 1-5 random books
            from home.factories.book import BookPageFactory

            num_books = random.randint(1, 5)
            for _ in range(num_books):
                book = BookPageFactory.create()
                obj.books.add(book)
