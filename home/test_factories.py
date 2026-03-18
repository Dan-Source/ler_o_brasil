"""
Tests specifically for factory functionality.
"""

from django.test import TestCase
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from home.factories import (
    AuthorPageFactory,
    BlogPostFactory,
    BookPageFactory,
    CategoryFactory,
    EventIndexPageFactory,
    EventPageFactory,
)
from home.models import (
    AuthorPage,
    BlogPost,
    BookPage,
    Category,
    EventIndexPage,
    EventPage,
)
from user.factories import UserFactory


class CategoryFactoryTests(TestCase):
    """Test CategoryFactory functionality."""

    def test_creates_valid_category(self):
        """Test that factory creates a valid category."""
        category = CategoryFactory.create()
        self.assertIsNotNone(category.pk)
        self.assertIsNotNone(category.name)
        self.assertIsNotNone(category.slug)

    def test_creates_batch(self):
        """Test batch creation."""
        categories = CategoryFactory.create_batch(5)
        self.assertEqual(len(categories), 5)
        self.assertEqual(Category.objects.count(), 5)


class BlogPostFactoryTests(WagtailPageTestCase):
    """Test BlogPostFactory functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_creates_valid_blogpost(self):
        """Test that factory creates a valid blog post."""
        blog_post = BlogPostFactory.create(parent=self.root_page)
        self.assertIsNotNone(blog_post.pk)
        self.assertIsNotNone(blog_post.title)
        self.assertIsNotNone(blog_post.owner)
        self.assertIsNotNone(blog_post.content)

    def test_creates_with_category(self):
        """Test creating blog post with category."""
        category = CategoryFactory.create()
        blog_post = BlogPostFactory.create(parent=self.root_page, category=category)
        self.assertEqual(blog_post.category, category)

    def test_creates_published_post(self):
        """Test published trait."""
        blog_post = BlogPostFactory.create(parent=self.root_page, published=True)
        self.assertTrue(blog_post.live)

    def test_creates_batch(self):
        """Test batch creation."""
        blog_posts = BlogPostFactory.create_batch(3, parent=self.root_page)
        self.assertEqual(len(blog_posts), 3)


class AuthorPageFactoryTests(WagtailPageTestCase):
    """Test AuthorPageFactory functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_creates_valid_author(self):
        """Test that factory creates a valid author page."""
        author = AuthorPageFactory.create(parent=self.root_page)
        self.assertIsNotNone(author.pk)
        self.assertIsNotNone(author.title)
        self.assertIsNotNone(author.owner)

    def test_creates_batch(self):
        """Test batch creation."""
        authors = AuthorPageFactory.create_batch(3, parent=self.root_page)
        self.assertEqual(len(authors), 3)


class BookPageFactoryTests(WagtailPageTestCase):
    """Test BookPageFactory functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_creates_valid_book(self):
        """Test that factory creates a valid book page."""
        book = BookPageFactory.create(parent=self.root_page)
        self.assertIsNotNone(book.pk)
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.owner)

    def test_creates_with_authors(self):
        """Test that books are created with authors."""
        book = BookPageFactory.create(parent=self.root_page)
        self.assertGreater(book.authors.count(), 0)

    def test_creates_with_specific_authors(self):
        """Test creating book with specific authors."""
        author1 = AuthorPageFactory.create(parent=self.root_page)
        author2 = AuthorPageFactory.create(parent=self.root_page)
        book = BookPageFactory.create(parent=self.root_page, authors=[author1, author2])
        self.assertEqual(book.authors.count(), 2)


class EventPageFactoryTests(WagtailPageTestCase):
    """Test EventPage and EventIndexPage factory functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root_page = Page.get_first_root_node()

    def test_creates_event_index_page(self):
        """Test creating event index page."""
        event_index = EventIndexPageFactory.create(parent=self.root_page)
        self.assertIsNotNone(event_index.pk)
        self.assertIsInstance(event_index, EventIndexPage)

    def test_creates_event_page(self):
        """Test creating event page with proper parent."""
        event = EventPageFactory.create()
        self.assertIsNotNone(event.pk)
        self.assertIsInstance(event, EventPage)
        self.assertIsInstance(event.get_parent().specific, EventIndexPage)

    def test_event_has_books(self):
        """Test that events are created with books."""
        event = EventPageFactory.create()
        self.assertGreater(event.books.count(), 0)

    def test_event_index_singleton(self):
        """Test that EventIndexPageFactory reuses existing index."""
        index1 = EventIndexPageFactory.create()
        index2 = EventIndexPageFactory.create()
        self.assertEqual(index1.pk, index2.pk)
