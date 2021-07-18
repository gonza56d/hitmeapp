# Python
from math import trunc
from typing import Dict

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
    price = models.DecimalField(max_digits=30, decimal_places=8)
    market_cap = models.DecimalField(max_digits=30, decimal_places=8)
    volume = models.DecimalField(max_digits=30, decimal_places=8)
    circulating_supply = models.DecimalField(max_digits=30, decimal_places=8)

    def set_attributes(self, result: Dict) -> None:
        factor = 10.0 ** 2
        self.rank = result.get('cmc_rank')
        self.price = trunc(float(result.get('quote').get('USD').get('price')) * factor) / factor
        self.market_cap = trunc(float(result.get('quote').get('USD').get('market_cap')) * factor) / factor
        self.volume = trunc(float(result.get('quote').get('USD').get('volume_24h')) * factor) / factor
        self.circulating_supply = trunc(float(result.get('circulating_supply')) * factor) / factor

    def __str__(self) -> str:
        return f'CryptoCurrency[crypto_currency={self.crypto_currency}, rank={self.rank}, price={self.price}, market_cap={self.market_cap}, volume={self.volume}, circulating_supply={self.circulating_supply}]'


class CryptoCurrencyManager(models.Manager):

    def get_with_current_value(self, symbol: str):
        _get = self.get(symbol=symbol)
        crypto_value = CryptoValue.objects.filter(crypto_currency=_get)
        print(crypto_value)
        if crypto_value:
            _get.current_value = crypto_value.latest()
        return _get

    def all_with_current_value(self):
        _all = self.all()
        for crypto_currency in _all:
            with_filter = CryptoValue.objects.filter(
                crypto_currency=crypto_currency
            )
            crypto_currency.rank = None
            if with_filter:
                latest = with_filter.latest()
                crypto_currency.current_value = latest
                crypto_currency.rank = latest.rank
        _all.order_by('cryptovalue__rank')
        return _all


class CryptoCurrency(BaseModel):
    """Some crypto currency in the market.
    """

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    current_price = float(0)

    def set_attributes(self, result: Dict) -> None:
        self.name = result.get('name')
        self.symbol = result.get('symbol')

    def __str__(self) -> str:
        return f'CryptoCurrency[symbol={self.symbol}, name={self.name}]'

    objects = CryptoCurrencyManager()
