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
        return CryptoCurrency(
            name=self.header.xpath('*//div/div[1]/div[1]/h2'),
            price='test',
            last_day='',
            last_week='',
            market_cap='',
            volume='',
            circulating_supply=''
        )

    def set_soup(self) -> None:
        curl = requests.get('https://coinmarketcap.com/currencies/' + self.currency)
        self.soup = BeautifulSoup(curl.text, 'html.parser')
        self.header = self.soup.find_all('div', {'class': 'sc-16r8icm-0'})[3]
        self.detail = self.soup.find('div', {'class': 'sc-16r8icm-0 nds9rn-0 cPoSGb'})

    def get_object(self, queryset=None) -> CryptoCurrency:
        self.set_soup()
        return self.build_asset()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.currency = kwargs['currency']
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)
