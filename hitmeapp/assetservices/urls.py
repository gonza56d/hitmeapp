"""Asset services urls."""

# Django
from django.urls import path

# Project
from .views import CryptoListView


urlpatterns = [
    path('crypto/', CryptoListView.as_view(), name='crypto')
]
