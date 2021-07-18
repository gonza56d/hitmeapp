# Project
from hitmeapp.taskapp.celery import app as celery_app
from .models import CryptoCurrency
from .views.crypto.external_requests import (
    DetailCryptoExternalRequest,
    ListCryptoExternalRequest
)


@celery_app.task
def collect_cryptos():
    _list = ListCryptoExternalRequest.get_list()
    for index, result in enumerate(_list):
        #try:
        crypto, created = CryptoCurrency.objects.get_or_create(
            symbol=result.symbol, name=result.name
        )
        print(result.name.replace(' ', '-'))
        crypto_value = DetailCryptoExternalRequest.build_asset(result)
        print('crypto_value:', crypto_value)
        crypto_value.rank = index + 1
        crypto_value = crypto
        crypto_value.save()
        #except IndexError as e:
        #    print('IndexError when collecting cryptos (task) at: ' + str(e))
