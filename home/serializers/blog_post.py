from rest_framework.serializers import ModelSerializer, SerializerMethodField

from home.models.author import AuthorPage
from home.models.blog_post import BlogPost
from home.serializers.author import AuthorPageSerializer


class BlogAuthorsSerializer(ModelSerializer):
    """Serializer for BlogPost author."""

    name = SerializerMethodField()

    class Meta:
        model = AuthorPage
        fields = ["id", "name", "avatar"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_avatar(self, obj):
        """Return the URL to the author profile image."""
        if obj.avatar:
            url = obj.avatar.get_rendition("fill-300x300").url
        request = self.context.get("request")
        return (
            request.build_absolute_uri(url) if request and url.startswith("/") else url
        )


class ListBlogPostSerializer(ModelSerializer):
    """Serializer for listing BlogPost instances."""

    author = SerializerMethodField()
    cover_image = SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "cover_image",
            "category",
            "excerpt",
            "featured_post",
            "slug",
            "author",
            "cover_image",
        ]

    def get_cover_image(self, obj):
        if not obj.cover_image:
            return None
        url = obj.cover_image.get_rendition("fill-300x450").url
        request = self.context.get("request")
        return (
            request.build_absolute_uri(url) if request and url.startswith("/") else url
        )

    def get_author(self, obj):
        """Return the author of the blog post."""
        author = AuthorPage.objects.filter(id=obj.author.id).first()
        return (
            AuthorPageSerializer(author, context=self.context).data if author else None
        )


class BlogPostSerializer(ModelSerializer):
    """Serializer for BlogPost model."""

    reading_time = SerializerMethodField()
    author = SerializerMethodField()
    cover_image = SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "cover_image",
            "category",
            "content",
            "reading_time",
            "featured_post",
            "slug",
            "author",
        ]

    def get_reading_time(self, obj):
        return obj.reading_time

    def get_cover_image(self, obj):
        if not obj.cover_image:
            return None
        url = obj.cover_image.get_rendition("fill-300x450").url
        request = self.context.get("request")
        return (
            request.build_absolute_uri(url) if request and url.startswith("/") else url
        )

    def get_author(self, obj):
        author = AuthorPage.objects.filter(id=obj.author.id).first()

        return (
            AuthorPageSerializer(author, context=self.context).data if author else None
        )
