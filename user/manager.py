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

    def create_superuser(self, email, password, **kwargs):
        """Create and saves a new super user."""
        account = self.create_account(email, password, **kwargs)
        account.is_active = True
        account.is_staff = True
        account.is_superuser = True
        account.save(using=self._db)
        return account
