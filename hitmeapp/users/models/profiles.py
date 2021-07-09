# Django
from django.db import models

# Project
from hitmeapp.utils.models import BaseModel, CommonRegex


class Profile(BaseModel):
    """
    Representation of users' profile.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, validators=[CommonRegex.LETTERS])
    last_name = models.CharField(max_length=100, validators=[CommonRegex.LETTERS])
    birthday = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='profiles', blank=True)
    bio = models.CharField(max_length=3000, null=True, blank=True)
