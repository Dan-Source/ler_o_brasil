from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from home.models.category import Category


class BlogPost(Page):
    """A blog post page model."""

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_posts",
    )
    excerpt = models.TextField(blank=True)
    content = RichTextField(blank=True)
    featured_post = models.BooleanField(
        default=False, help_text="Mark as featured post"
    )

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
        FieldPanel("content", classname="full"),
        FieldPanel("excerpt"),
        FieldPanel("category"),
        FieldPanel("featured_post"),
    ]

    @property
    def reading_time(self):
        """Estimate reading time based on word count."""
        AVERAGE_WORDS_PER_MINUTE = 200
        word_count = len(self.content.split())
        reading_speed_wpm = AVERAGE_WORDS_PER_MINUTE
        return max(1, word_count // reading_speed_wpm)

    @property
    def published_at(self):
        """Return the published date of the blog post."""
        return self.first_published_at

    @property
    def author(self):
        """Return the author of the blog post."""
        return self.owner

    @property
    def cover_image_url(self):
        """Return the URL of the cover image if it exists, otherwise return None."""
        if self.cover_image:
            return self.cover_image.get_rendition("fill-300x450").url
        return None
