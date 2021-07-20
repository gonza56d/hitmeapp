# Django
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.views.generic import View

# Project
from hitmeapp.assetservices.models import CryptoTracking


class CryptoTrackingDeleteView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        crypto_tracking_id = kwargs['crypto_tracking_id']
        crypto_tracking = CryptoTracking.objects.get(id=crypto_tracking_id)
        if crypto_tracking.user == request.user:
            crypto_tracking.delete()
            messages.success(request, _(f'{crypto_tracking.crypto_currency.name} is no longer being tracked'))
        return redirect('users:my-profile')
