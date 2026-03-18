import factory
import wagtail_factories
from wagtail.models import Page

from home.factories.category import CategoryFactory
from home.models import BlogPost
from user.factories import UserFactory


class BlogPostFactory(wagtail_factories.PageFactory):
    """Factory for creating BlogPost instances."""

    class Meta:
        model = BlogPost

    title = factory.Faker("sentence", nb_words=6, locale="pt_BR")
    excerpt = factory.Faker("paragraph", locale="pt_BR")
    content = factory.Faker("text", max_nb_chars=2000, locale="pt_BR")
    owner = factory.SubFactory(UserFactory)

    # 70% chance to have a category
    category = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=70),
        yes_declaration=factory.SubFactory(CategoryFactory),
        no_declaration=None,
    )

    # 60% chance to have a cover image
    cover_image = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=60),
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

    class Params:
        published = factory.Trait(
            live=True,
        )

    @factory.post_generation
    def publish_page(obj, create, extracted, **kwargs):
        """Publish the page if the 'published' trait is used."""
        if not create:
            return

        if extracted or (hasattr(obj, "live") and obj.live):
            revision = obj.save_revision()
            revision.publish()
