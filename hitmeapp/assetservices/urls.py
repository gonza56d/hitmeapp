"""Asset services urls."""

# Django
from django.urls import path

# Project
from .views import CryptoListView, CryptoDetailView


urlpatterns = [
    path('crypto/', CryptoListView.as_view(), name='crypto-list'),
    path('crypto/<str:currency>', CryptoDetailView.as_view(), name='crypto-detail')
]
