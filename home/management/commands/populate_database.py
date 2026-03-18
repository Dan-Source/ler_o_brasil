"""
Management command to populate the database with test data using factories.

Usage:
    python manage.py populate_database
    python manage.py populate_database --users 10 --categories 20
    python manage.py populate_database --blogposts 50 --published
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from home.factories import (
    AuthorPageFactory,
    BlogPostFactory,
    BookPageFactory,
    CategoryFactory,
    EventIndexPageFactory,
    EventPageFactory,
)
from user.factories import UserFactory


class Command(BaseCommand):
    help = "Populate the database with test data using factories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="Number of users to create (default: 5)",
        )
        parser.add_argument(
            "--categories",
            type=int,
            default=10,
            help="Number of categories to create (default: 10)",
        )
        parser.add_argument(
            "--blogposts",
            type=int,
            default=20,
            help="Number of blog posts to create (default: 20)",
        )
        parser.add_argument(
            "--authors",
            type=int,
            default=15,
            help="Number of author pages to create (default: 15)",
        )
        parser.add_argument(
            "--books",
            type=int,
            default=30,
            help="Number of book pages to create (default: 30)",
        )
        parser.add_argument(
            "--events",
            type=int,
            default=10,
            help="Number of event pages to create (default: 10)",
        )
        parser.add_argument(
            "--published",
            action="store_true",
            help="Publish all blog posts (default: mixed draft/published)",
        )
        parser.add_argument(
            "--superuser",
            action="store_true",
            help="Create at least one superuser",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting database population..."))

        try:
            with transaction.atomic():
                # Create users
                self.stdout.write("Creating users...")
                users_count = options["users"]

                if options["superuser"]:
                    # Create at least one superuser
                    UserFactory.create(
                        username="admin",
                        email="admin@example.com",
                        superuser=True,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            "  ✓ Created superuser: admin (password: testpass123)"
                        )
                    )
                    users_count -= 1

                UserFactory.create_batch(users_count)
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created {users_count} regular users")
                )

                # Create categories
                self.stdout.write("Creating categories...")
                categories = CategoryFactory.create_batch(options["categories"])
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created {len(categories)} categories")
                )

                # Create author pages
                self.stdout.write("Creating author pages...")
                authors = AuthorPageFactory.create_batch(options["authors"])
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created {len(authors)} author pages")
                )

                # Create blog posts
                self.stdout.write("Creating blog posts...")
                if options["published"]:
                    blog_posts = BlogPostFactory.create_batch(
                        options["blogposts"],
                        published=True,
                    )
                else:
                    # Mix of published and draft
                    published_count = options["blogposts"] // 2
                    draft_count = options["blogposts"] - published_count

                    published_posts = BlogPostFactory.create_batch(
                        published_count,
                        published=True,
                    )
                    draft_posts = BlogPostFactory.create_batch(draft_count)
                    blog_posts = published_posts + draft_posts

                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created {len(blog_posts)} blog posts")
                )

                # Create book pages
                self.stdout.write("Creating book pages...")
                books = BookPageFactory.create_batch(options["books"])
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created {len(books)} book pages")
                )

                # Create event index page and event pages
                self.stdout.write("Creating event pages...")
                event_index = EventIndexPageFactory.create()
                events = EventPageFactory.create_batch(
                    options["events"],
                    parent=event_index,
                )
                self.stdout.write(self.style.SUCCESS("  ✓ Created event index page"))
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created {len(events)} event pages")
                )

                # Summary
                self.stdout.write("")
                self.stdout.write(self.style.SUCCESS("=" * 50))
                self.stdout.write(
                    self.style.SUCCESS("Database population completed successfully!")
                )
                self.stdout.write(self.style.SUCCESS("=" * 50))
                self.stdout.write(
                    self.style.SUCCESS(f"Total users: {options['users']}")
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Total categories: {len(categories)}")
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Total blog posts: {len(blog_posts)}")
                )
                self.stdout.write(self.style.SUCCESS(f"Total authors: {len(authors)}"))
                self.stdout.write(self.style.SUCCESS(f"Total books: {len(books)}"))
                self.stdout.write(self.style.SUCCESS(f"Total events: {len(events)}"))

                if options["superuser"]:
                    self.stdout.write("")
                    self.stdout.write(self.style.WARNING("Superuser credentials:"))
                    self.stdout.write("  Username: admin")
                    self.stdout.write("  Password: testpass123")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during population: {str(e)}"))
            raise
