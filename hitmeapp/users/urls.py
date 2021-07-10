"""Users urls."""

# Django
from django.urls import path

# Project
from hitmeapp.users.views import signup


urlpatterns = [
    path('signup', signup, name='signup')
]
