# Django
from django.db import models

# Project
from hitmeapp.utils.models import BaseModel


class CryptoCurrency(BaseModel):
    """Model to build instances to display in crypto currency views.
    """

    rank = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    market_cap = models.DecimalField(max_digits=9, decimal_places=2)
    volume = models.DecimalField(max_digits=9, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=9, decimal_places=2)
