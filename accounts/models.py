# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        FIELD_AGENT = 'FIELD_AGENT', 'Field Agent'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.FIELD_AGENT
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_field_agent(self):
        return self.role == self.Role.FIELD_AGENT

    def save(self, *args, **kwargs):
        # Automatically sync is_staff with the ADMIN role
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        else:
            # Optional: Revoke staff access if demoted to Field Agent
            self.is_staff = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"