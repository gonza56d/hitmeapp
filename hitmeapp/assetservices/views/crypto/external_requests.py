"""External services requests for crypto currencies."""

# Python
import requests

# BS4
from bs4 import BeautifulSoup

# Project
from hitmeapp.assetservices.models import CryptoCurrency
from hitmeapp.utils.generic_functions import currency_to_float


class ListCryptoExternalRequest:
    
    @classmethod
    def build_asset_from_row(cls, number, row) -> CryptoCurrency:
        asset = None
        try:
            asset = CryptoCurrency(
                number=number,
                name=row.find_all('p')[1].text,
                price=currency_to_float(row.find_all('td')[3].text)
            )
        except IndexError:
            asset = CryptoCurrency(
                number=number,
                name=row.find_all('td')[2].find_all('span')[1].text,
                price=currency_to_float(row.find_all('td')[3].text)
            )
        return asset

    @classmethod
    def set_soup(cls):
        curl = requests.get('https://coinmarketcap.com/')
        cls.soup = BeautifulSoup(curl.text, 'html.parser')
        cls.table_rows = cls.soup.find('tbody').find_all('tr')

    @classmethod
    def get_list(cls):
        cls.set_soup()
        _list = []
        for index, row in enumerate(cls.table_rows):
            _list.append(cls.build_asset_from_row(index+1, row))
        return _list
