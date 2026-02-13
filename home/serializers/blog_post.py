from rest_framework.serializers import ModelSerializer, SerializerMethodField

from home.models.blog_post import BlogPost


class BlogPostSerializer(ModelSerializer):
    """Serializer for BlogPost model."""

    reading_time = SerializerMethodField()

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
        ]

    def get_reading_time(self, obj):
        return obj.reading_time
