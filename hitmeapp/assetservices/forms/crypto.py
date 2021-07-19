"""Crypto currencies forms."""

# Django
from django import forms
from django.utils.translation import gettext as _

# Project
from ..models import CryptoTracking, CryptoCurrency


class CryptoTrackingForm(forms.ModelForm):

    class Meta:
        model = CryptoTracking
        fields = [
            'crypto_currency',
            'desired_value_type',
            'desired_value',
            'notification_platform'
        ]

    def __init__(self, crypto: CryptoCurrency=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['crypto_currency'].widget = forms.HiddenInput()
        self.fields['crypto_currency'].label = ''
        self.fields['crypto_currency'].initial = crypto
        self.fields['desired_value_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['desired_value_type'].label = _('Track price changes by')
        self.fields['desired_value'].widget.attrs.update({'class': 'form-control'})
        self.fields['desired_value'].label = _('Notify me when the price changed by')
        self.fields['notification_platform'].widget.attrs.update({'class': 'form-control'})
        self.fields['notification_platform'].label = _('Notify me in')
