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
    ContactMessage,
)
from user.factories import UserFactory


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

    def test_list_endpoint_filters_by_category_slug(self):
        """Test list endpoint filters blog posts by category slug."""
        matching_category = CategoryFactory.create(
            name="Eligendi",
            slug="eligendi",
        )
        other_category = CategoryFactory.create(name="Outro", slug="outro")

        matching_post = BlogPostFactory.create(
            parent=self.root_page,
            category=matching_category,
            published=True,
        )
        BlogPostFactory.create(
            parent=self.root_page,
            category=other_category,
            published=True,
        )

        response = self.client.get(
            reverse("blogpost-list"),
            {"category": "eligendi"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], matching_post.id)

    def test_list_endpoint_filters_by_author_id(self):
        """Test list endpoint filters blog posts by author id."""
        matching_author = UserFactory.create()
        other_author = UserFactory.create()

        matching_post = BlogPostFactory.create(
            parent=self.root_page,
            owner=matching_author,
            published=True,
        )
        BlogPostFactory.create(
            parent=self.root_page,
            owner=other_author,
            published=True,
        )

        response = self.client.get(
            reverse("blogpost-list"),
            {"author": matching_author.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], matching_post.id)

    def test_list_endpoint_filters_by_multiple_author_ids(self):
        """Test list endpoint supports comma-separated author IDs."""
        author_1 = UserFactory.create()
        author_2 = UserFactory.create()
        author_3 = UserFactory.create()

        post_1 = BlogPostFactory.create(
            parent=self.root_page,
            owner=author_1,
            published=True,
        )
        post_2 = BlogPostFactory.create(
            parent=self.root_page,
            owner=author_2,
            published=True,
        )
        BlogPostFactory.create(
            parent=self.root_page,
            owner=author_3,
            published=True,
        )

        response = self.client.get(
            reverse("blogpost-list"),
            {"author": f"{author_1.id},{author_2.id},invalid"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)
        result_ids = {item["id"] for item in response.data["results"]}
        self.assertEqual(result_ids, {post_1.id, post_2.id})

    def test_list_endpoint_respects_page_size_query_param(self):
        """Test list endpoint uses page_size from query params."""
        category = CategoryFactory.create(name="Eligendi", slug="eligendi")
        BlogPostFactory.create_batch(
            7,
            parent=self.root_page,
            category=category,
            published=True,
        )

        response = self.client.get(
            reverse("blogpost-list"),
            {"page": 1, "page_size": 6, "category": "eligendi"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 7)
        self.assertEqual(len(response.data["results"]), 6)

    def test_search_endpoint_returns_matching_blog_posts(self):
        """Test search endpoint returns only blog posts matching query."""
        matching_post = BlogPostFactory.create(
            parent=self.root_page,
            title="Poetry from Recife",
            published=True,
        )
        BlogPostFactory.create(
            parent=self.root_page,
            title="Cooking tips",
            published=True,
        )

        response = self.client.get(
            reverse("blogpost-search"),
            {"query": "Poetry"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], matching_post.id)

    def test_search_endpoint_returns_empty_results_when_query_missing(self):
        """Test search endpoint empty payload when query is missing."""
        BlogPostFactory.create(
            parent=self.root_page,
            title="Poetry from Recife",
            published=True,
        )

        response = self.client.get(reverse("blogpost-search"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(response.data["results"], [])


class GenericPageSearchApiTests(APITestCase):
    """Tests for generic page search API endpoint."""

    def setUp(self):
        self.root_page = Page.get_first_root_node()

    def test_generic_search_returns_blog_author_and_book(self):
        blog_post = BlogPostFactory.create(
            parent=self.root_page,
            title="Recife Literário",
            search_description="Resumo de blog em Recife.",
            published=True,
        )
        author = AuthorPageFactory.create(
            parent=self.root_page,
            title="Autor Recife",
            search_description="Bio curta do autor.",
        )
        author.save_revision().publish()

        book = BookPageFactory.create(
            parent=self.root_page,
            title="Livro Recife",
            search_description="Resumo do livro.",
        )
        book.save_revision().publish()

        response = self.client.get(
            reverse("generic-page-search"),
            {"query": "Recife"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertIn(
            {
                "title": blog_post.title,
                "search_description": blog_post.search_description,
                "slug": blog_post.slug,
            },
            response.data["results"],
        )
        self.assertIn(
            {
                "title": author.title,
                "search_description": author.search_description,
                "slug": None,
            },
            response.data["results"],
        )
        self.assertIn(
            {
                "title": book.title,
                "search_description": book.search_description,
                "slug": None,
            },
            response.data["results"],
        )

    def test_generic_search_returns_empty_results_when_query_missing(self):
        BlogPostFactory.create(
            parent=self.root_page,
            title="Recife Literário",
            published=True,
        )

        response = self.client.get(reverse("generic-page-search"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(response.data["results"], [])


class ContactMessageApiTests(APITestCase):
    """Tests for contact message API endpoint."""

    def test_contact_message_post_success(self):
        payload = {
            "name": "Ana Silva",
            "email": "ana@example.com",
            "subject": "Duvida sobre livros",
            "message": "Gostaria de saber sobre os proximos lancamentos.",
        }

        response = self.client.post(reverse("contact-message"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {"message": "Contact message received successfully."},
        )
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved_message = ContactMessage.objects.first()
        self.assertEqual(saved_message.name, payload["name"])
        self.assertEqual(saved_message.email, payload["email"])
        self.assertEqual(saved_message.subject, payload["subject"])
        self.assertEqual(saved_message.message, payload["message"])

    def test_contact_message_post_invalid_payload(self):
        payload = {
            "name": "Ana Silva",
            "email": "not-an-email",
            "subject": "Duvida",
            "message": "Mensagem",
        }

        response = self.client.post(reverse("contact-message"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "Invalid contact message payload."},
        )


class CsrfTokenApiTests(APITestCase):
    """Tests for CSRF bootstrap endpoint."""

    def test_csrf_endpoint_sets_cookie(self):
        response = self.client.get(reverse("csrf-token"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "CSRF cookie set."})
        self.assertIn("csrftoken", response.cookies)


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


class AuthorPageApiTests(APITestCase):
    """Tests for Author API list and detail endpoints."""

    def setUp(self):
        self.root_page = Page.get_first_root_node()

    def test_authors_list_endpoint_returns_published_authors(self):
        author_1 = AuthorPageFactory.create(parent=self.root_page)
        author_1.save_revision().publish()

        author_2 = AuthorPageFactory.create(parent=self.root_page)
        author_2.save_revision().publish()

        response = self.client.get(reverse("author-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_authors_detail_endpoint_returns_author_by_slug(self):
        author = AuthorPageFactory.create(parent=self.root_page)
        author.save_revision().publish()

        response = self.client.get(
            reverse("author-detail", kwargs={"slug": author.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], author.id)
        self.assertEqual(response.data["title"], author.title)


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
