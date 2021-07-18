# Django
from django.db.utils import DataError

# Project
from hitmeapp.taskapp.celery import app as celery_app
from .models import CryptoCurrency
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
