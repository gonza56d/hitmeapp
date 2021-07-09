# Django
from django.db import models


class BaseModel(models.Model):
    """
    Base model that adds utility fields such as time created and last time
    modified.
    """

    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
