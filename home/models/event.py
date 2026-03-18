from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class EventIndexPage(Page):
    """A page that lists all events in a calendar format."""

    description = RichTextField(
        blank=True, help_text="Description for the events calendar page"
    )

    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
    ]

    subpage_types = ["home.EventPage"]

    def get_events(self):
        """Get all event child pages ordered by date."""
        return (
            EventPage.objects.live().child_of(self).order_by("event_date", "event_time")
        )

    def __str__(self):
        return self.title


class EventPage(Page):
    """A page for an event."""

    description = RichTextField(blank=True, help_text="Description of the event")
    event_date = models.DateField(help_text="Date when the event will happen")
    event_time = models.TimeField(
        null=True, blank=True, help_text="Time when the event will happen"
    )
    event_link = models.URLField(
        blank=True,
        help_text="Link for video call or event details (e.g., Zoom, Meet, etc.)",
    )
    books = models.ManyToManyField(
        "home.BookPage",
        related_name="events",
        blank=True,
        help_text="Select all books related to this event",
    )

    content_panels = Page.content_panels + [
        FieldRowPanel(
            [
                FieldPanel("event_date"),
                FieldPanel("event_time"),
            ]
        ),
        FieldPanel("event_link"),
        FieldPanel("description", classname="full"),
        FieldPanel("books"),
    ]

    parent_page_types = ["home.EventIndexPage"]

    def __str__(self):
        return f"{self.title} ({self.event_date})"
