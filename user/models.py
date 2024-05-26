# Django
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator, URLValidator

from user.manager import CustomBaseUserManager


class Qualification(models.Model):
    GRADE_TYPE_CHOICES = [
        (4.0, '4.0 Scale'),
        (5.0, '5.0 Scale'),
        ('Percentage', 'Percentage'),
    ]

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='qualifications')
    university = models.CharField(max_length=255)
    degree = models.CharField(max_length=50, choices=[(
        'BS', 'Bachelor of Science'), ('MS', 'Master of Science'), ('PhD', 'Doctor of Philosophy')])
    institute = models.CharField(max_length=255)
    grade_type = models.CharField(
        max_length=20, choices=GRADE_TYPE_CHOICES, default=4.0)
    grade = models.FloatField(default=0.0)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    major = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.degree} from {self.institute}"


class Experience(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company}"


class Project(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Skill(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Social(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='socials')
    url = models.URLField(validators=[URLValidator()])

    def __str__(self):
        return self.url


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    resume = models.FileField(upload_to='resumes/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'docx'])], blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomBaseUserManager()

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "user"
