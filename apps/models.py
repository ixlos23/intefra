import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Model, CharField, DateField, ManyToManyField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove the username field
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = []  # Don't need 'username' as a required field

    objects = UserManager()  # Set the custom manager


class Film(Model):
    title = CharField(max_length=250)
    release_date = DateField(default=datetime.date.today)
    genre = ManyToManyField("apps.Genre", related_name="films")


class Genre(Model):
    name = CharField(max_length=250)

    def __str__(self):
        return self.name
