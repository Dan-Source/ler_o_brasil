from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from home.views.api import AuthorPageViewSet, BookPageViewSet, EventPageViewSet
from home.views.blog_post import BlogPostViewSet
from home.views.category import CategoryViewSet, category_create

router = routers.DefaultRouter()
router.register(r"blog-posts", BlogPostViewSet, basename="blogpost")
router.register(r"blog-categories", CategoryViewSet, basename="blogcategory")
router.register(r"authors", AuthorPageViewSet, basename="author")
router.register(r"books", BookPageViewSet, basename="book")
router.register(r"events", EventPageViewSet, basename="event")

home_urls = [
    path("api/v1/", include(router.urls)),
]
