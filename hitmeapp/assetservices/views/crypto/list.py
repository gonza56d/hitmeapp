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
from hitmeapp.assetservices.models import CryptoCurrency


class CryptoListView(LoginRequiredMixin, ListView):

    template_name = 'crypto/list.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object_list = CryptoCurrency.objects.all_with_current_value()
        context = self.get_context_data()
        return self.render_to_response(context)
