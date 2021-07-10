# Django
from django.contrib.auth.models import AbstractUser
from django.db import models

# Project
from hitmeapp.utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """
    User accounts model.
    """

    email = models.EmailField(
        unique=True,
        error_messages={'unique': 'Email already in use.'}
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
