"""Users urls."""

# Django
from django.urls import path

# Project
from hitmeapp.users.views import SignupView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup')
]
