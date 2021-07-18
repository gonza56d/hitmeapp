"""External services requests for crypto currencies."""

# Python
import requests
from typing import List

# Project
from config.settings.base import COINMARKETCAP_API_KEY
from hitmeapp.assetservices.models import CryptoCurrency, CryptoValue


class ListCryptoExternalRequest:
    """Handle external requests to list cryptos.
    """

    def __init__(self) -> None:
        self.endpoint = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.secret_api_key = {'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}
        self.accept = {'Accept': 'application/json'}
        self.start = {'start': '1'}
        self.limit = {'limit': '100'}
        self.convert = {'convert': 'USD'}

    @property
    def headers(self):
        return {**self.secret_api_key, **self.accept}

    @property
    def body(self):
        return {**self.start, **self.limit, **self.convert}

    def get_list(self) -> List[CryptoValue]:
        """Get list of cryptos from https://coinmarketcap.com/.

        Return
        ------
        List[CryptoValueSerializer] : list of crypto values serializer instances.
        """
        request = requests.get(self.endpoint, headers=self.headers, params=self.body)
        results = []
        for result in request.json().get('data'):
            currency = CryptoCurrency()
            currency.set_attributes(result)
            value = CryptoValue()
            value.crypto_currency = currency
            value.set_attributes(result)
            results.append(value)
        return results
