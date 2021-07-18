# REST Framework
from rest_framework import serializers

# Project
from hitmeapp.assetservices.models.crypto import CryptoCurrency, CryptoValue


class CryptoCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = CryptoCurrency
        fields = ['symbol', 'name']


class CryptoValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = CryptoValue
        fields = ['crypto_currency', 'rank', 'price', 'market_cap', 'volume', 'circulating_supply']

    crypto_currency = CryptoCurrencySerializer()
