# Django
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models, transaction

# Project
from .profiles import Profile
from hitmeapp.utils.models import BaseModel, CommonRegex


class UserManager(DjangoUserManager):

    def _create_user(self, username, email, password, first_name, last_name, 
                     **extra_fields):
        """
        Ensure username and email are in lowercase before calling the framework
        implementation of method.
        """
        if not first_name or not last_name:
            raise ValueError('First name and last name are required.')
        username = username or ''
        username = username.lower()
        email = email or ''
        email = email.lower()
        with transaction.atomic():
            user = super()._create_user(username, email, password, **extra_fields)
            Profile.objects.create(
                user = user,
                first_name = first_name,
                last_name = last_name
            )
        return user

    def create_user(self, username, email=None, password=None, first_name=None,
                    last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, first_name, 
                                 last_name, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, first_name='Admin', 
                                 last_name='Admin', **extra_fields)


class User(BaseModel, AbstractUser):
    """
    User accounts model.
    """

    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[CommonRegex.LOWERCASE_AND_NUMBERS],
        error_messages={'unique': 'Username already in use.'}
    )
    email = models.EmailField(
        unique=True,
        error_messages={'unique': 'Email already in use.'}
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
