# Django
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.manager import CustomBaseUserManager


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_owner = models.BooleanField(default=False)

    objects = CustomBaseUserManager()

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "user"
