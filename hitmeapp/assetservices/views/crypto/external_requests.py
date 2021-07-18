"""External services requests for crypto currencies."""

# Python
import re
import requests
from typing import List

# BS4
from bs4 import BeautifulSoup
from bs4.element import Tag

# Project
from hitmeapp.assetservices.models import CryptoCurrency, CryptoValue
from hitmeapp.utils.generic_functions import currency_to_float


class DetailCryptoExternalRequest:
    """Handle external requests to get the detail information of a single crypto.
    """

    @classmethod
    def get_circulating_supply(cls) -> float:
        if cls.is_data_tracked:
            return currency_to_float(cls.header.find_all('div', {'class': 'statsValue___2iaoZ'})[4].text)
        else:
            return None

    @classmethod
    def get_volume(cls) -> float:
        if cls.is_data_tracked:
            return currency_to_float(cls.header.find_all('div', {'class': 'statsValue___2iaoZ'})[2].text)
        else:
            return None

    @classmethod
    def get_market_cap(cls) -> float:
        if cls.is_data_tracked:
            return currency_to_float(cls.header.find_all('div', {'class': 'statsValue___2iaoZ'})[0].text)
        else:
            return None

    @classmethod
    def get_price(cls) -> float:
        if cls.is_data_tracked:
            return currency_to_float(cls.header.find('div', {'class': 'priceValue___11gHJ'}).text)
        else:
            return cls.currency.current_price

    @classmethod
    def check_is_data_tracked(cls) -> None:
        """Check if the currency is currently being tracked by coinmarketcap
        and set is_data_tracked.
        """
        try:
            text = cls.header.find_all('h2', {'class': '1q9q90x-0'})[2].text
            cls.is_data_tracked = 'untracked' in text
        except IndexError or AttributeError:
            cls.is_data_tracked = False

    @classmethod
    def build_asset(cls, currency: CryptoCurrency) -> CryptoValue:
        """Create CryptoValue object from a currency detail in 
        https://coinmarketcap.com/currencies/$CURRENCY/.

        Parameters
        ----------
        currency : str
            Name of the crypto currency to look for.
        
        Return
        ------
        CryptoCurrency : instance to display the crypto info.
        """
        cls.set_soup(currency)
        cls.check_is_data_tracked()
        asset = CryptoValue(
            price=cls.get_price(),
            market_cap=cls.get_market_cap(),
            volume=cls.get_volume(),
            circulating_supply=cls.get_circulating_supply()
        )
        asset.crypto_currency = currency
        return asset

    @classmethod
    def set_soup(cls, currency: CryptoCurrency) -> None:
        """Perform get request to https://coinmarketcap.com/currencies/$CURRENCY/
        and set the BeautifulSoup instance with the result.
        """
        cls.currency = currency
        curl = requests.get('https://coinmarketcap.com/currencies/' 
            + currency.name.replace(' ', '-').replace('.', '-'))
        cls.soup = BeautifulSoup(curl.text, 'html.parser')
        cls.header = cls.soup.select('div[class*="container"]')[3]
        cls.symbol = cls.header.find('small', {'class': 'nameSymbol___1arQV'}).text

    @classmethod
    def clean(cls):
        del cls.is_data_tracked, cls.soup, cls.currency, cls.header, cls.symbol


class ListCryptoExternalRequest:
    """Handle external requests to list cryptos.
    """

    @classmethod
    def get_current_price(cls) -> float:
        return currency_to_float(cls.row.find_all('td')[3].text)

    @classmethod
    def get_name(cls) -> str:
        if cls.dummy_row:
            return cls.row.find_all('td')[2].find_all('span')[1].text
        else:
            return cls.row.find_all('td')[2].find_all('p')[0].text

    @classmethod
    def get_symbol(cls) -> str:
        if cls.dummy_row:
            return cls.row.find_all('td')[2].find_all('span')[2].text
        else:
            return cls.row.find_all('td')[2].find_all('p')[1].text

    @classmethod
    def check_row(cls) -> None:
        row_class = cls.row.get('class') or ''
        cls.dummy_row = 'sc-1rqmhtg-0' in row_class

    @classmethod
    def build_asset_from_row(cls, row: Tag) -> CryptoCurrency:
        """Create CryptoCurrency object from a https://coinmarketcap.com/
        table row.

        Parameters
        ----------
        row : Tag
            bs4 Tag instance. Row from https://coinmarketcap.com/ table.
        
        Return
        ------
        CryptoCurrency : instance to display the crypto info.
        """
        cls.row = row
        cls.check_row()
        asset = CryptoCurrency(
            symbol=cls.get_symbol(),
            name=cls.get_name()
        )
        asset.current_price=cls.get_current_price()
        row = None
        cls.dummy_row = None
        return asset

    @classmethod
    def set_soup(cls) -> None:
        """Perform get request to https://coinmarketcap.com/ and set the
        BeautifulSoup instance with the result and find all the table rows
        referencing them to cls.table_rows.
        """
        curl = requests.get('https://coinmarketcap.com/')
        cls.soup = BeautifulSoup(curl.text, 'html.parser')
        cls.table_rows = cls.soup.find('tbody').find_all('tr')

    @classmethod
    def get_list(cls) -> List[CryptoCurrency]:
        """Get list of cryptos from https://coinmarketcap.com/.

        Return
        ------
        List[CryptoCurrency] : list of CryptoCurrency instances.
        """
        cls.set_soup()
        _list = []
        for row in cls.table_rows:
            _list.append(cls.build_asset_from_row(row))
        return _list
