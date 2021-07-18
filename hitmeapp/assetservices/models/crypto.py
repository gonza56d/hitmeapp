# Django
from django.db import models

# Project
from hitmeapp.utils.models import BaseModel


class CryptoValue(BaseModel):
    """Value at some datetime of a specific CryptoCurrency.
    """

    crypto_currency = models.ForeignKey(
        'assetservices.CryptoCurrency', on_delete=models.CASCADE, null=False
    )
    rank = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    market_cap = models.DecimalField(max_digits=14, decimal_places=2)
    volume = models.DecimalField(max_digits=14, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=14, decimal_places=2)


class CryptoCurrency(BaseModel):
    """Some crypto currency in the market.
    """

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    current_price = float(0)

    def __str__(self) -> str:
        return f'CryptoCurrency[rank={self.rank}, name={self.name}, price={self.price}]'
