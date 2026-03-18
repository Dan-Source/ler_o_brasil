from rest_framework import serializers

from home.models import AuthorPage


class AuthorPageSerializer(serializers.ModelSerializer):
    """Serializer for AuthorPage model."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = AuthorPage
        fields = [
            "id",
            "title",
            "description",
            "birth_year",
            "url",
        ]

    def get_url(self, obj):
        """Return the URL to the author page."""
        return obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None
