from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from home.models.blog_post import BlogPost
from home.serializers.blog_post import (
    BlogPostSerializer,
    ListBlogPostSerializer,
)


class BlogPostViewSet(ReadOnlyModelViewSet):
    """ViewSet for viewing blog posts."""

    serializer_class = ListBlogPostSerializer
    detail_serializer_class = BlogPostSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        """Use detail serializer for detail-oriented endpoints."""
        if self.action in ["retrieve", "featured"]:
            return self.detail_serializer_class
        return self.serializer_class

    def get_queryset(self):
        return BlogPost.objects.live().public()

    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        """Return the most recently published featured blog post."""
        featured_post = (
            self.get_queryset()
            .filter(featured_post=True)
            .order_by("-first_published_at")
            .first()
        )

        if featured_post is None:
            raise NotFound("No featured blog post found.")

        serializer = self.get_serializer(featured_post)
        return Response(serializer.data)
