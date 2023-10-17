from __future__ import annotations

from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models

from choices_fields.fields import IntegerChoicesArrayField, TextChoicesArrayField


class CustomUser(AbstractUser):
    """Custom User subclass."""

    class UserType(models.TextChoices):
        OWNER = "owner", "Account owner"
        ADMIN = "admin", "Administrator"
        USER = "user", "User"

    class UserStatus(models.IntegerChoices):
        ONE = 1, "One"
        TWO = 2, "Two"
        THREE = 3, "Three"

    user_type = TextChoicesArrayField(choices=UserType.choices)
    user_status = IntegerChoicesArrayField(
        choices=UserStatus.choices,
        widget=forms.CheckboxSelectMultiple,
    )
