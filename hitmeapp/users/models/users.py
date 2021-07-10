# Django
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models, transaction

# Project
from .profiles import Profile
from hitmeapp.utils.models import BaseModel


class UserManager(DjangoUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Ensure username and email are in lowercase before calling the framework
        implementation of method.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(BaseModel, AbstractUser):
    """
    User accounts model.
    """

    email = models.EmailField(
        unique=True,
        error_messages={'unique': 'Email already in use.'}
    )
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
