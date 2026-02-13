from rest_framework.viewsets import ReadOnlyModelViewSet

from home.models.blog_post import BlogPost
from home.serializers.blog_post import BlogPostSerializer


class BlogPostViewSet(ReadOnlyModelViewSet):
    """ViewSet for viewing blog posts."""

    queryset = BlogPost.objects.live().public()
    serializer_class = BlogPostSerializer
