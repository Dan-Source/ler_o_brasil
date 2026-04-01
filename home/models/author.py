from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class AuthorPage(Page):
    """A page for an author profile."""

    avatar = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Author profile image",
    )

    description = RichTextField(
        help_text="Biography and description of the author",
        blank=True,
    )
    birth_year = models.IntegerField(
        null=True, blank=True, help_text="Year of birth (optional)"
    )

    content_panels = Page.content_panels + [
        FieldPanel("avatar"),
        FieldPanel("birth_year"),
        FieldPanel("description", classname="full"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.title
