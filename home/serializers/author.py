from rest_framework import serializers

from home.models import AuthorPage


class AuthorPageSerializer(serializers.ModelSerializer):
    """Serializer for AuthorPage model."""

    url = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = AuthorPage
        fields = [
            "id",
            "title",
            "description",
            "birth_year",
            "avatar",
            "url",
        ]

    def get_avatar(self, obj):
        """Return the URL to the author profile image."""
        if obj.avatar:
            url = obj.avatar.get_rendition("fill-300x300").url
            request = self.context.get("request")
            return (
                request.build_absolute_uri(url)
                if request and url.startswith("/")
                else url
            )

    def get_url(self, obj):
        """Return the URL to the author page."""
        return obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None
