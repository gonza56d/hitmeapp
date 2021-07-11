"""Views for detailing crypto currency asset services."""

# Python
from io import StringIO
from typing import Any
import requests

# Django
from django.views.generic.detail import DetailView
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# BS4 and lxml
from bs4 import BeautifulSoup
from lxml import etree

# Project
from hitmeapp.assetservices.models import CryptoCurrency


class CryptoDetailView(DetailView):

    template_name = 'crypto/detail.html'

    def build_asset(self) -> CryptoCurrency:
        symbol = self.header.find('small', {'class': 'nameSymbol___1arQV'}).text
        self.header.find('small', {'class': 'nameSymbol___1arQV'}).decompose()
        return CryptoCurrency(
            number=self.header.find('div', {'class': 'namePill___3p_Ii namePillPrimary___2-GWA'}).text,
            name=self.header.find('h2', {'class': 'sc-1q9q90x-0 iYFMbU h1___3QSYG'}).text + ' (' + symbol + ')',
            price=self.header.find('div', {'class': 'priceValue___11gHJ'}).text,
            last_day=self.detail.find_all('span', {'class': 'sc-15yy2pl-0 kAXKAX'})[0].text,
            last_week='',
            market_cap=self.header.find_all('div', {'class': 'statsValue___2iaoZ'})[0].text,
            volume=self.header.find_all('div', {'class': 'statsValue___2iaoZ'})[2].text,
            circulating_supply=self.header.find_all('div', {'class': 'statsValue___2iaoZ'})[4].text
        )

    def set_soup(self) -> None:
        curl = requests.get('https://coinmarketcap.com/currencies/' + self.currency)
        self.soup = BeautifulSoup(curl.text, 'html.parser')
        self.header = self.soup.find('div', {'class': 'sc-16r8icm-0 dOJIkS container___lbFzk'})
        self.detail = self.soup.find('div', {'class': 'sc-16r8icm-0 nds9rn-0 cPoSGb'})
        print(self.header)

    def get_object(self, queryset=None) -> CryptoCurrency:
        self.set_soup()
        return self.build_asset()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.currency = kwargs['currency']
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)
