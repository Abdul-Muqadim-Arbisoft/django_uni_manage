from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser class.

    This model includes the default user fields provided by AbstractUser and adds custom
    fields for the user's email address, father's name, description, software engineering experience,
    and the timestamp of the last profile update.
    """

    email = models.EmailField('email address', unique=True)  # User's email address, must be unique
    father_name = models.CharField(max_length=100)  # User's father's name
    description = models.TextField(null=True, blank=True)  # Description or bio for the user
    software_engineering_experience = \
        models.PositiveIntegerField(null=True, blank=True)  # User's software engineering experience in years
    last_profile_update = models.DateTimeField(null=True, blank=True)  # Timestamp of the last profile update

    USERNAME_FIELD = 'email'  # Email will be used as the username
    REQUIRED_FIELDS = ['username', 'father_name']  # These fields are required when creating a user

    def save(self, *args, **kwargs):
        """
        Override the save method to update custom fields.

        If the software_engineering_experience field is not provided, it will be set to 0,
        and the last_profile_update field will be updated with the current timestamp.
        """
        if self.software_engineering_experience is None:
            self.software_engineering_experience = 0  # Default value if not provided
        self.last_profile_update = timezone.now()  # Update the timestamp
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        """Return the email address as the string representation of the user."""
        return self.email
