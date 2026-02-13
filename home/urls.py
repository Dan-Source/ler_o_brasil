from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from home.views.blog_post import BlogPostViewSet

router = routers.DefaultRouter()
router.register(r"blog-posts", BlogPostViewSet, basename="blogpost")

home_urls = [
    path("api/v1/", include(router.urls)),
]
