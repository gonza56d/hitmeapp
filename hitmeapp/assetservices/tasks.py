# Python
from datetime import timedelta

# Project
from hitmeapp.taskapp.celery import app as celery_app
from .views.crypto.external_requests import (
    DetailCryptoExternalRequest,
    ListCryptoExternalRequest
)


@celery_app.task
def collect_cryptos():
    _list = ListCryptoExternalRequest.get_list()
    for result in _list:
        try:
            crypto = DetailCryptoExternalRequest.build_asset(result.name)
            crypto.save()
        except IndexError as e:
            print('IndexError when collecting cryptos (task) at: ' + str(e))
