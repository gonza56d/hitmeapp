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

# Project
from hitmeapp.assetservices.forms import CryptoTrackingForm
from hitmeapp.assetservices.models import CryptoCurrency


class CryptoDetailView(LoginRequiredMixin, DetailView):

    template_name = 'crypto/detail.html'

    def get_object(self, queryset=None) -> CryptoCurrency:
        return CryptoCurrency.objects.get_with_current_value(symbol=self.currency)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.currency = kwargs['currency']
        self.object = self.get_object()
        context = self.get_context_data()
        context['crypto_tracking_form'] = CryptoTrackingForm(self.object)
        return self.render_to_response(context)
