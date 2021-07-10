"""Crypto currency asset service views."""

# Python
import requests
from typing import Any

# Django
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import ListView

# BS4
from bs4 import BeautifulSoup

# Project
from hitmeapp.assetservices.models import CryptoCurrency
from hitmeapp.utils.generic_functions import currency_to_float


class CryptoListView(ListView):

    template_name = 'crypto/list.html'

    def set_soup(self):
        curl = requests.get('https://coinmarketcap.com/')
        self.soup = BeautifulSoup(curl.text, 'html.parser')
        self.table_body = self.soup.find('tbody')
        self.table_rows = self.table_body.find_all('tr')
    
    def get_object_list(self):
        self.set_soup()
        objects_list = []
        for i, row in enumerate(self.table_rows):
            print(row)
            print(i)
            objects_list.append(CryptoCurrency(
                number=row.find_all('p')[0].text,
                name=row.find_all('p', {'class': 'sc-1eb5slv-0'})[1].text,
                price=currency_to_float(row.find_all('a', {'class': 'cmc-link'})[1].text),
                last_day=currency_to_float(row.find_all('span', {'class': 'sc-15yy2pl-0'})[0].text),
                last_week=currency_to_float(row.find_all('span', {'class': 'sc-15yy2pl-0'})[1].text),
                market_cap=currency_to_float(row.find('span', {'class': 'sc-1ow4cwt-1'}).text),
                volume=currency_to_float(row.find_all('p', {'font-size': '1'})[3].text),
                circulating_supply=row.find_all('p', {'font-size': '1'})[4].text
            ))
        return objects_list

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object_list = self.get_object_list()
        context = self.get_context_data()
        return self.render_to_response(context)
