"""Views for listing crypto currency asset services."""

# Python
from typing import Any

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic.list import ListView

# Project
from .external_requests import ListCryptoExternalRequest
from hitmeapp.assetservices.models import CryptoCurrency


class CryptoListView(LoginRequiredMixin, ListView):

    template_name = 'crypto/list.html'
    external_requests = ListCryptoExternalRequest

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        currencies = CryptoCurrency.objects.annotate(occurrences=Count('name'))
        currencies = set([c.name for c in currencies])
        self.object_list = []
        for currency in currencies:
            self.object_list.append(CryptoCurrency.objects.filter(name=currency).latest())
        self.object_list.sort(key=lambda x: x.rank)
        context = self.get_context_data()
        return self.render_to_response(context)
