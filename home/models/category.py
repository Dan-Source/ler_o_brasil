from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class Category(models.Model):
    """Model representing a blog post category."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name
