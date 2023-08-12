from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.constants import EMAIL_FIELD_NAME, REQUIRED_USER_FIELDS
from utils.helpers import update_user_profile_fields


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser class.

    This model includes the default user fields provided by AbstractUser and adds custom
    fields for the user's email address, father's name, description, software engineering experience,
    and the timestamp of the last profile update.
    """
    email = models.EmailField('email address', unique=True)
    father_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    software_engineering_experience = models.PositiveIntegerField(null=True, blank=True)
    last_profile_update = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = EMAIL_FIELD_NAME
    REQUIRED_FIELDS = REQUIRED_USER_FIELDS

    def save(self, *args, **kwargs):
        """
        Override the save method to update custom fields.
        """
        update_user_profile_fields(self)
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the email address as the string representation of the user."""
        return self.email
