from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class BlogPost(Page):
    """A blog post page model."""

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    category = models.CharField(max_length=255, blank=True)
    content = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("content", classname="full"),
    ]

    @property
    def reading_time(self):
        """Estimate reading time based on word count."""
        AVERAGE_WORDS_PER_MINUTE = 200
        word_count = len(self.content.split())
        reading_speed_wpm = AVERAGE_WORDS_PER_MINUTE
        return max(1, word_count // reading_speed_wpm)
