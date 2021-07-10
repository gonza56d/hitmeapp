"""Users urls."""

# Django
from django.urls import path

# Project
from hitmeapp.users.views import SignupView, LoginView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
