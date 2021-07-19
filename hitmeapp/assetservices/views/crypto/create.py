# Django
from hitmeapp.assetservices.models.crypto import CryptoCurrency
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import View

# Project
from hitmeapp.assetservices.models import CryptoTracking
from hitmeapp.assetservices.forms.crypto import CryptoTrackingForm
from hitmeapp.utils.generic_functions import form_errors_into_string


class CryptoTrackingCreateView(View):

    def post(self, request):
        form = CryptoTrackingForm(data=request.POST)
        if form.is_valid():
            crypto = form.cleaned_data.get('crypto_currency')
            CryptoCurrency.objects.set_current_value(crypto)
            crypto_tracking = CryptoTracking(
                user=request.user,
                crypto_currency=crypto,
                desired_value_type=form.cleaned_data.get('desired_value_type'),
                desired_value=form.cleaned_data.get('desired_value'),
                notification_platform=form.cleaned_data.get('notification_platform'),
                value_when_tracked=crypto.current_value.price
            )
            crypto_tracking.save()
            messages.success(request, _(f'{crypto.name} ({crypto.symbol}) tracked'))
        else:
            messages.warning(request, form.errors)
        return redirect('assetservices:crypto-list')
