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


class CryptoDetailView(LoginRequiredMixin, DetailView):

    template_name = 'crypto/detail.html'

    def get_object(self, queryset=None) -> CryptoCurrency:
        return CryptoCurrency.objects.filter(name=self.currency).latest()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.currency = kwargs['currency']
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)
