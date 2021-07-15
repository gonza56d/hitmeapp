"""External services requests for crypto currencies."""

# Python
import re
import requests
from typing import List

# BS4
from bs4 import BeautifulSoup
from bs4.element import Tag

# Project
from hitmeapp.assetservices.models import CryptoCurrency
from hitmeapp.utils.generic_functions import currency_to_float


class DetailCryptoExternalRequest:
    """Handle external requests to get the detail information of a single crypto.
    """

    @classmethod
    def build_asset(cls, currency: str) -> CryptoCurrency:
        """Create CryptoCurrency object from a currency detail in 
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
        symbol = cls.header.find('small', {'class': 'nameSymbol___1arQV'}).text
        cls.header.find('small', {'class': 'nameSymbol___1arQV'}).decompose()
        return CryptoCurrency(
            rank=int(re.sub('[^0-9]', '', cls.header.find('div', {'class': 'namePill___3p_Ii namePillPrimary___2-GWA'}).text)),
            name=cls.header.find('h2', {'class': 'sc-1q9q90x-0'}).text + ' (' + symbol + ')',
            price=currency_to_float(cls.header.find('div', {'class': 'priceValue___11gHJ'}).text),
            market_cap=currency_to_float(cls.header.find_all('div', {'class': 'statsValue___2iaoZ'})[0].text),
            volume=currency_to_float(cls.header.find_all('div', {'class': 'statsValue___2iaoZ'})[2].text),
            circulating_supply=currency_to_float(cls.header.find_all('div', {'class': 'statsValue___2iaoZ'})[4].text)
        )

    @classmethod
    def set_soup(cls, currency: str) -> None:
        """Perform get request to https://coinmarketcap.com/currencies/$CURRENCY/
        and set the BeautifulSoup instance with the result.
        """
        curl = requests.get('https://coinmarketcap.com/currencies/' + currency)
        cls.soup = BeautifulSoup(curl.text, 'html.parser')
        cls.header = cls.soup.find_all('div', {'class': 'container'})[3]


class ListCryptoExternalRequest:
    """Handle external requests to list cryptos.
    """
    
    @classmethod
    def build_asset_from_row(cls, number: int, row: Tag) -> CryptoCurrency:
        """Create CryptoCurrency object from a https://coinmarketcap.com/
        table row.

        Parameters
        ----------
        number : int
            Position of the row plus one to assign to the instance number attr.
        
        row : Tag
            bs4 Tag instance. Row from https://coinmarketcap.com/ table.
        
        Return
        ------
        CryptoCurrency : instance to display the crypto info.
        """
        asset = None
        try:
            asset = CryptoCurrency(
                rank=number,
                name=row.find_all('p')[1].text,
                price=currency_to_float(row.find_all('td')[3].text)
            )
        except IndexError:
            asset = CryptoCurrency(
                rank=number,
                name=row.find_all('td')[2].find_all('span')[1].text,
                price=currency_to_float(row.find_all('td')[3].text)
            )
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
        for index, row in enumerate(cls.table_rows):
            _list.append(cls.build_asset_from_row(index+1, row))
        return _list
