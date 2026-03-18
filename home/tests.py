from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from home.factories import (
    AuthorPageFactory,
    BlogPostFactory,
    BookPageFactory,
    CategoryFactory,
)
from home.models import (
    AuthorPage,
    BlogPost,
    BookPage,
    Category,
)


class BlogPostTests(WagtailPageTestCase):
    """
    Tests for BlogPost model and factory.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_blogpost_creation_with_factory(self):
        """Test that BlogPostFactory creates valid blog posts."""
        blog_post = BlogPostFactory.create(parent=self.root_page)
        self.assertIsInstance(blog_post, BlogPost)
        self.assertIsNotNone(blog_post.title)
        self.assertIsNotNone(blog_post.owner)

    def test_blogpost_with_category(self):
        """Test blog post with category relationship."""
        category = CategoryFactory.create(name="Literatura")
        blog_post = BlogPostFactory.create(
            parent=self.root_page,
            category=category,
        )
        self.assertEqual(blog_post.category, category)

    def test_blogpost_reading_time_property(self):
        """Test reading_time calculated property."""
        blog_post = BlogPostFactory.create(
            parent=self.root_page,
            content="word " * 200,  # 200 words
        )
        self.assertEqual(blog_post.reading_time, 1)

    def test_published_blogpost(self):
        """Test creating a published blog post."""
        blog_post = BlogPostFactory.create(
            parent=self.root_page,
            published=True,
        )
        self.assertTrue(blog_post.live)


class BlogPostApiTests(APITestCase):
    """Tests for BlogPost API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_featured_endpoint_returns_featured_blog_post(self):
        """Test featured endpoint returns the latest featured blog post."""
        BlogPostFactory.create(
            parent=self.root_page,
            title="Older featured post",
            slug="older-featured-post",
            featured_post=True,
            published=True,
        )
        latest_featured_post = BlogPostFactory.create(
            parent=self.root_page,
            title="Latest featured post",
            slug="latest-featured-post",
            featured_post=True,
            published=True,
        )
        BlogPostFactory.create(
            parent=self.root_page,
            title="Regular post",
            slug="regular-post",
            featured_post=False,
            published=True,
        )

        response = self.client.get(reverse("blogpost-featured"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], latest_featured_post.id)
        self.assertEqual(response.data["slug"], latest_featured_post.slug)
        self.assertTrue(response.data["featured_post"])
        self.assertIn("content", response.data)
        self.assertIn("reading_time", response.data)

    def test_featured_endpoint_returns_404_when_no_featured_post_exists(self):
        """Test featured endpoint returns 404 when no featured post exists."""
        BlogPostFactory.create(
            parent=self.root_page,
            title="Regular post",
            slug="regular-post",
            featured_post=False,
            published=True,
        )

        response = self.client.get(reverse("blogpost-featured"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryTests(TestCase):
    """
    Tests for Category model and factory.
    """

    def test_category_creation_with_factory(self):
        """Test that CategoryFactory creates valid categories."""
        category = CategoryFactory.create()
        self.assertIsInstance(category, Category)
        self.assertIsNotNone(category.name)
        self.assertIsNotNone(category.slug)

    def test_category_unique_slug(self):
        """Test that slugs are unique when names collide."""
        CategoryFactory.create(name="test")
        category2 = CategoryFactory.create(name="test")
        self.assertNotEqual(category2.slug, "test")


class AuthorPageTests(WagtailPageTestCase):
    """
    Tests for AuthorPage model and factory.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_authorpage_creation_with_factory(self):
        """Test that AuthorPageFactory creates valid author pages."""
        author = AuthorPageFactory.create(parent=self.root_page)
        self.assertIsInstance(author, AuthorPage)
        self.assertIsNotNone(author.title)
        self.assertIsNotNone(author.owner)


class BookPageTests(WagtailPageTestCase):
    """
    Tests for BookPage model and factory.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_bookpage_creation_with_factory(self):
        """Test that BookPageFactory creates valid book pages."""
        book = BookPageFactory.create(parent=self.root_page)
        self.assertIsInstance(book, BookPage)
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.owner)

    def test_bookpage_with_authors(self):
        """Test that books are created with authors."""
        book = BookPageFactory.create(parent=self.root_page)
        self.assertGreater(book.authors.count(), 0)
