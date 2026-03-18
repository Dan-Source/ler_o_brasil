from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class BookPage(Page):
    """A page for a book."""

    subtitle = models.CharField(
        max_length=300, blank=True, help_text="Optional subtitle"
    )
    description = RichTextField(
        blank=True, help_text="Detailed description of the book"
    )
    publication_year = models.IntegerField(
        null=True, blank=True, help_text="Year of publication"
    )
    book_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category or type of book (e.g., Fiction, Reference, etc.)",
    )
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Book cover image",
    )
    authors = models.ManyToManyField(
        "home.AuthorPage",
        related_name="books",
        blank=True,
        help_text="Select all authors for this book",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("publication_year"),
        FieldPanel("book_type"),
        FieldPanel("cover_image"),
        FieldPanel("description", classname="full"),
        FieldPanel("authors"),
    ]

    def __str__(self):
        return self.title
