# Django
from django.urls import path
# Project
from .views import index


urlpatterns = [
    path('', index, name='main'),
]
