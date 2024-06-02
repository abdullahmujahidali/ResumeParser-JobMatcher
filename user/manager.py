# Django
from django.contrib.auth.models import BaseUserManager


class CustomBaseUserManager(BaseUserManager):
    """A Manager class for BaseUser."""

    def create_account(self, email, password=None, **extra_fields):
        """Creates & saves a new user."""
        if not email:
            raise ValueError("Users must have an email address!")
        account = self.model(email=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email, password, **extra_fields):
        """Create and saves a new super user."""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_account(email, password, **extra_fields)
