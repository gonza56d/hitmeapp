"""Asset services urls."""

# Django
from django.urls import path

# Project
from .views import (
    CryptoListView,
    CryptoDetailView,
    CryptoTrackingCreateView,
    CryptoTrackingDeleteView
)


urlpatterns = [
    path('crypto/', CryptoListView.as_view(), name='crypto-list'),
    path('crypto/<str:currency>', CryptoDetailView.as_view(), name='crypto-detail'),
    path('crypto/tracking/create/', CryptoTrackingCreateView.as_view(), name='crypto-tracking-create'),
    path('crypto/tracking/delete/<int:crypto_tracking_id>', CryptoTrackingDeleteView.as_view(), name='crypto-tracking-delete'),
]
