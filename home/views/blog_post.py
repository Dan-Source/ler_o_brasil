from rest_framework.viewsets import ReadOnlyModelViewSet

from home.models.blog_post import BlogPost
from home.serializers.blog_post import BlogPostSerializer


class BlogPostViewSet(ReadOnlyModelViewSet):
    """ViewSet for viewing blog posts."""

    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.live().public()
