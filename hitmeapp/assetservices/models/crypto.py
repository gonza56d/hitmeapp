# Python
from math import trunc
from typing import Dict

# Django
from django.db import models

# Project
from hitmeapp.utils.models import BaseModel
from hitmeapp.utils.models.custom_fields import CurrencyField


class CryptoTracking(BaseModel):
    """Describe which users are tracking which Cryptos.
    """

    class DesiredValueType(models.TextChoices):
        PERCENTAGE = 'P', 'Percentage'
        VALUE = 'V', 'Value'

    class NotificationPlatform(models.TextChoices):
        EMAIL = 'E', 'Email'
        TELE = 'T', 'Telegram'
        WPP = 'W', 'WhatsApp'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    crypto_currency = models.ForeignKey(
        'assetservices.CryptoCurrency', on_delete=models.CASCADE, null=False
    )
    value_when_tracked = CurrencyField()
    desired_value_type = models.CharField(
        max_length=1, choices=DesiredValueType.choices, blank=False
    )
    desired_value = CurrencyField()
    notification_platform = models.CharField(
        max_length=1, choices=NotificationPlatform.choices, blank=False
    )

    def __str__(self) -> str:
        return f'CryptoTracking[user={self.user}, crypto_currency={self.crypto_currency}, value_when_tracked={self.value_when_tracked}, desired_value_type={self.desired_value_type}, desired_value={self.desired_value}, notification_platform={self.notification_platform}]'


class CryptoValue(BaseModel):
    """Value at some datetime of a specific CryptoCurrency.
    """

    crypto_currency = models.ForeignKey(
        'assetservices.CryptoCurrency', on_delete=models.CASCADE, null=False
    )
    rank = models.PositiveIntegerField()
    price = CurrencyField()
    market_cap = CurrencyField()
    volume = CurrencyField()
    circulating_supply = CurrencyField()
    percent_change_1h = CurrencyField()
    percent_change_24h = CurrencyField()
    percent_change_7d = CurrencyField()
    percent_change_30d = CurrencyField()
    percent_change_60d = CurrencyField()
    percent_change_90d = CurrencyField()

    FACTOR = 10.0 ** 2

    def truncate(self, value: float) -> float:
        if value is None:
            return 0.0
        return trunc(float(value) * self.FACTOR) / self.FACTOR

    @property
    def truncated_price(self) -> float:
        return self.truncate(self.price)

    @property
    def truncated_market_cap(self) -> float:
        return self.truncate(self.market_cap)

    @property
    def truncated_volume(self) -> float:
        return self.truncate(self.volume)

    @property
    def truncated_circulating_supply(self) -> float:
        return self.truncate(self.circulating_supply)

    def set_attributes(self, result: Dict) -> None:
        self.rank = result.get('cmc_rank')
        self.circulating_supply = self.truncate(float(result.get('circulating_supply')))
        self.volume = self.truncate(float(result.get('quote').get('USD').get('volume_24h')))
        self.price = self.truncate(float(result.get('quote').get('USD').get('price')))
        self.market_cap = self.truncate(float(result.get('quote').get('USD').get('market_cap')))
        self.percent_change_1h = self.truncate(float(result.get('quote').get('USD').get('percent_change_1h')))
        self.percent_change_24h = self.truncate(float(result.get('quote').get('USD').get('percent_change_24h')))
        self.percent_change_7d = self.truncate(float(result.get('quote').get('USD').get('percent_change_7d')))
        self.percent_change_30d = self.truncate(float(result.get('quote').get('USD').get('percent_change_30d')))
        self.percent_change_60d = self.truncate(float(result.get('quote').get('USD').get('percent_change_60d')))
        self.percent_change_90d = self.truncate(float(result.get('quote').get('USD').get('percent_change_90d')))

    def __str__(self) -> str:
        return f'CryptoCurrency[crypto_currency={self.crypto_currency}, rank={self.rank}, price={self.price}, market_cap={self.market_cap}, volume={self.volume}, circulating_supply={self.circulating_supply}]'


class CryptoCurrencyManager(models.Manager):

    def set_current_value(self, crypto_currency) -> None:
        crypto_value = CryptoValue.objects.filter(crypto_currency=crypto_currency).latest()
        crypto_currency.current_value = crypto_value

    def get_with_current_value(self, symbol: str):
        _get = self.get(symbol=symbol)
        crypto_value = CryptoValue.objects.filter(crypto_currency=_get)
        if crypto_value:
            _get.current_value = crypto_value.latest()
        return _get

    def all_with_current_value(self):
        _all = self.all()
        for crypto_currency in _all:
            latest = CryptoValue.objects.filter(
                crypto_currency=crypto_currency
            ).latest()
            crypto_currency.rank = None
            if latest:
                crypto_currency.current_value = latest
                crypto_currency.rank = latest.rank
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
