"""AssetServices models admin."""

# Django
from django.contrib import admin

# Project
from .models import CryptoCurrency, CryptoValue


@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):

    list_display = ('symbol', 'name')
    search_fields = ('symbol', 'name')
    list_filter = ('symbol', 'name')


@admin.register(CryptoValue)
class CryptoValueAdmin(admin.ModelAdmin):

    list_display = ('crypto_currency', 'rank', 'price', 'market_cap', 'volume', 'circulating_supply')
    search_fields = ('crypto_currency', 'rank', 'price', 'market_cap', 'volume', 'circulating_supply')
    list_filter = ('crypto_currency', 'rank', 'price', 'market_cap', 'volume', 'circulating_supply')
