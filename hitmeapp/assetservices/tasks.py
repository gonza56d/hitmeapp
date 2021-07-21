# Python
from typing import List

# Project
from hitmeapp.taskapp.celery import app as celery_app
from .models import CryptoCurrency, CryptoTracking
from .api.crypto.external_requests import ListCryptoExternalRequest


@celery_app.task
def collect_cryptos():
    _list = ListCryptoExternalRequest().get_list()
    for result in _list:
        crypto, created = CryptoCurrency.objects.get_or_create(
            symbol=result.crypto_currency.symbol,
            name=result.crypto_currency.name
        )
        result.crypto_currency = crypto
        result.save()


def send_crypto_trackings(ready_for_alerts: List[CryptoTracking]) -> None:
    for alert in ready_for_alerts:
        pass # TODO send it
        alert.sent = True
    for alert in ready_for_alerts:
        if alert.sent:
            alert.delete()


@celery_app.task
def check_crypto_trackings():
    currencies = CryptoCurrency.objects.all_with_current_value()
    trackings = CryptoTracking.objects.select_related('users')\
        .select_related('crypto_currency').all()
    ready_for_alerts = []
    for tracking in trackings:
        for currency in currencies:
            if tracking.crypto_currency == currency:
                if currency.current_value >= tracking.desired_value > tracking.value_when_tracked \
                or currency.current_value <= tracking.desired_value < tracking.value_when_tracked:
                    ready_for_alerts.append(tracking)

