from rest_framework.viewsets import ReadOnlyModelViewSet

from home.models.blog_post import BlogPost
from home.serializers.blog_post import BlogPostSerializer, ListBlogPostSerializer


class BlogPostViewSet(ReadOnlyModelViewSet):
    """ViewSet for viewing blog posts."""

    serializer_class = ListBlogPostSerializer
    detail_serializer_class = BlogPostSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return BlogPost.objects.live().public()
