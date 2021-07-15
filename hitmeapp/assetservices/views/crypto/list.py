"""Views for listing crypto currency asset services."""

# Python
from typing import Any

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic.list import ListView

# Project
from .external_requests import ListCryptoExternalRequest


class CryptoListView(LoginRequiredMixin, ListView):

    template_name = 'crypto/list.html'
    external_requests = ListCryptoExternalRequest

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object_list = self.external_requests.get_list()
        context = self.get_context_data()
        return self.render_to_response(context)
