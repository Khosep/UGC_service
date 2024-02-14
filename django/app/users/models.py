"""Модели приложения users."""
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from movies.constants import CHARFIELD_MAX_LENGTH


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=CHARFIELD_MAX_LENGTH,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(
        max_length=CHARFIELD_MAX_LENGTH, blank=True, null=True
    )
    last_name = models.CharField(
        max_length=CHARFIELD_MAX_LENGTH, blank=True, null=True
    )
    roles = ArrayField(
        models.CharField(max_length=CHARFIELD_MAX_LENGTH), default=list
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = MyUserManager()

    def __str__(self):
        return f"{self.email} {self.id}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
