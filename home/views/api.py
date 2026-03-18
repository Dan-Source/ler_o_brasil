from rest_framework import viewsets

from home.models import AuthorPage, BookPage, EventPage
from home.serializers.author import AuthorPageSerializer
from home.serializers.book import BookPageDetailSerializer, BookPageListSerializer
from home.serializers.event import EventPageDetailSerializer, EventPageListSerializer


class AuthorPageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AuthorPage model with read-only access."""

    queryset = AuthorPage.objects.live()
    serializer_class = AuthorPageSerializer


class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for BookPage model with read-only access."""

    queryset = BookPage.objects.live()

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "retrieve":
            return BookPageDetailSerializer
        return BookPageListSerializer


class EventPageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for EventPage model with read-only access."""

    queryset = EventPage.objects.live().order_by("event_date", "event_time")

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "retrieve":
            return EventPageDetailSerializer
        return EventPageListSerializer
