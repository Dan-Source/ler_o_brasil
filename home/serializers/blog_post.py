from rest_framework.serializers import ModelSerializer, SerializerMethodField

from home.models.blog_post import BlogPost
from ler_o_brasil import settings
from user.models import User


class BlogAuthorsSerializer(ModelSerializer):
    """Serializer for BlogPost author."""

    name = SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ListBlogPostSerializer(ModelSerializer):
    """Serializer for listing BlogPost instances."""

    author = BlogAuthorsSerializer()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "cover_image",
            "category",
            "excerpt",
            "slug",
            "author",
        ]


class BlogPostSerializer(ModelSerializer):
    """Serializer for BlogPost model."""

    reading_time = SerializerMethodField()
    author = BlogAuthorsSerializer()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "cover_image",
            "category",
            "content",
            "reading_time",
            "slug",
            "author",
        ]

    def get_reading_time(self, obj):
        return obj.reading_time
