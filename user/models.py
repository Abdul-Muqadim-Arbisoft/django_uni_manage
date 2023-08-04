from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    father_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    software_engineering_experience = models.PositiveIntegerField(null=True, blank=True)
    last_profile_update = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'father_name']

    def save(self, *args, **kwargs):
        if self.software_engineering_experience is None:
            self.software_engineering_experience = 0  # Default value if not provided
        self.last_profile_update = timezone.now()  # Update the timestamp
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
