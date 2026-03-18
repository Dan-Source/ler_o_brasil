from rest_framework import serializers

from home.models import EventPage
from home.serializers.book import BookPageListSerializer


class EventPageListSerializer(serializers.ModelSerializer):
    """List view serializer for EventPage model."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = EventPage
        fields = [
            "id",
            "title",
            "event_date",
            "event_time",
            "event_link",
            "url",
        ]

    def get_url(self, obj):
        """Return the URL to the event page."""
        return obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None


class EventPageDetailSerializer(serializers.ModelSerializer):
    """Detail view serializer for EventPage model."""

    books = BookPageListSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = EventPage
        fields = [
            "id",
            "title",
            "description",
            "event_date",
            "event_time",
            "event_link",
            "url",
            "books",
        ]

    def get_url(self, obj):
        """Return the URL to the event page."""
        return obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None
