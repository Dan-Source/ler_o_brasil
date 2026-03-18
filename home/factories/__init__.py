"""
Factories for creating test data and populating the database.

Usage:
    from home.factories import BlogPostFactory, CategoryFactory

    # Create a single instance
    blog_post = BlogPostFactory.create()

    # Create multiple instances
    categories = CategoryFactory.create_batch(5)

    # Create with custom values
    blog_post = BlogPostFactory.create(
        title='Custom Title',
        category=my_category
    )

    # Create a published blog post
    blog_post = BlogPostFactory.create(published=True)
"""

from .author import AuthorPageFactory
from .blog_post import BlogPostFactory
from .book import BookPageFactory
from .category import CategoryFactory
from .event import EventIndexPageFactory, EventPageFactory

__all__ = [
    "CategoryFactory",
    "BlogPostFactory",
    "AuthorPageFactory",
    "BookPageFactory",
    "EventIndexPageFactory",
    "EventPageFactory",
]
