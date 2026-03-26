from rest_framework import serializers
from wagtail.models import Page

from home.models import BlogPost


class GenericPageSearchSerializer(serializers.ModelSerializer):
    """Serializer for generic page search results."""

    slug = serializers.SerializerMethodField()

    def get_slug(self, obj):
        return obj.slug if isinstance(obj.specific, BlogPost) else None

    class Meta:
        model = Page
        fields = ["title", "search_description", "slug"]
