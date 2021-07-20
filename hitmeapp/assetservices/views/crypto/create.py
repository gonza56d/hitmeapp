# Django
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import View

# Project
from hitmeapp.assetservices.forms.crypto import CryptoTrackingForm
from hitmeapp.assetservices import services
from hitmeapp.utils.generic_functions import form_errors_into_string


class CryptoTrackingCreateView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle user POST request when tries to create a new CryptoTracking.
        """
        form = CryptoTrackingForm(data=request.POST)
        if form.is_valid():
            crypto = services.create_crypto_tracking(
                user=request.user,
                crypto_currency=form.cleaned_data.get('crypto_currency'),
                desired_value=form.cleaned_data.get('desired_value'),
                desired_value_type=form.cleaned_data.get('desired_value_type'),
                notification_platform=form.cleaned_data.get('notification_platform')
            )
            if crypto:
                messages.success(request, _(f'{crypto.crypto_currency.name} ({crypto.crypto_currency.symbol}) is now being tracked'))
            else:
                messages.error(request, _('Something went wrong'))
        else:
            errors = form_errors_into_string(form.errors)
            messages.warning(request, errors)
        return redirect('assetservices:crypto-list')
