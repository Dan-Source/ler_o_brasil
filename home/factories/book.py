import random

import factory
import wagtail_factories
from wagtail.models import Page

from home.models import BookPage
from user.factories import UserFactory


class BookPageFactory(wagtail_factories.PageFactory):
    """Factory for creating BookPage instances."""

    class Meta:
        model = BookPage

    title = factory.Faker("sentence", nb_words=4, locale="pt_BR")
    subtitle = factory.Faker("sentence", nb_words=8, locale="pt_BR")
    description = factory.Faker("paragraph", locale="pt_BR")
    publication_year = factory.Faker("year")
    book_type = factory.Iterator(
        ["romance", "poesia", "conto", "ensaio", "crônica", "infantil"]
    )
    owner = factory.SubFactory(UserFactory)

    # 80% chance to have a cover image
    cover_image = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=80),
        yes_declaration=factory.SubFactory(wagtail_factories.ImageFactory),
        no_declaration=None,
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override create to handle Wagtail Page tree structure."""
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

    @factory.post_generation
    def authors(obj, create, extracted, **kwargs):
        """Add authors to the book after creation."""
        if not create:
            return

        if extracted:
            # If a list of authors was passed, use it
            for author in extracted:
                obj.authors.add(author)
        else:
            # Otherwise, create 1-3 random authors
            from home.factories.author import AuthorPageFactory

            num_authors = random.randint(1, 3)
            for _ in range(num_authors):
                author = AuthorPageFactory.create()
                obj.authors.add(author)
