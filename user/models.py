from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    country = models.CharField(verbose_name="country", max_length=255)
