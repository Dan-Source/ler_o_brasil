from rest_framework import serializers

from home.models import BookPage
from home.serializers.author import AuthorPageSerializer


class BookPageListSerializer(serializers.ModelSerializer):
    """List view serializer for BookPage model."""

    authors = AuthorPageSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = BookPage
        fields = [
            "id",
            "title",
            "subtitle",
            "publication_year",
            "book_type",
            "url",
            "authors",
        ]

    def get_url(self, obj):
        """Return the URL to the book page."""
        return obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None


class BookPageDetailSerializer(serializers.ModelSerializer):
    """Detail view serializer for BookPage model."""

    authors = AuthorPageSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = BookPage
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "publication_year",
            "book_type",
            "cover_image_url",
            "url",
            "authors",
        ]

    def get_cover_image_url(self, obj):
        """Return the URL to the cover image."""
        if obj.cover_image:
            return obj.cover_image.get_rendition("fill-300x450").url
        return None

    def get_url(self, obj):
        """Return the URL to the book page."""
        return obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None
