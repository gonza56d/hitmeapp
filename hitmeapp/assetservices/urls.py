"""Asset services urls."""

# Django
from django.urls import path

# Project
from .views import crypto_view


urlpatterns = [
    path('crypto/', crypto_view, name='crypto')
]
