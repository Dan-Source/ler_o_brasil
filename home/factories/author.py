import factory
import wagtail_factories
from wagtail.models import Page

from home.models import AuthorPage
from user.factories import UserFactory


class AuthorPageFactory(wagtail_factories.PageFactory):
    """Factory for creating AuthorPage instances."""

    class Meta:
        model = AuthorPage

    title = factory.Faker("name", locale="pt_BR")
    description = factory.Faker("paragraph", locale="pt_BR")
    birth_year = factory.Faker("year")
    owner = factory.SubFactory(UserFactory)

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
