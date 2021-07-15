"""Views for detailing crypto currency asset services."""

# Python
from io import StringIO
from typing import Any
import requests

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# BS4 and lxml
from bs4 import BeautifulSoup

# Project
from hitmeapp.assetservices.models import CryptoCurrency
from .external_requests import DetailCryptoExternalRequest


class CryptoDetailView(LoginRequiredMixin, DetailView):

    template_name = 'crypto/detail.html'
    external_requests = DetailCryptoExternalRequest

    def get_object(self, queryset=None) -> CryptoCurrency:
        return self.external_requests.build_asset(self.currency)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.currency = kwargs['currency'].lower().replace(' ', '-')
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)
