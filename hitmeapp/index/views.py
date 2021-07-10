"""Index views"""

# Django
from django.shortcuts import render

# Project
from hitmeapp.users.forms import SignupForm


def index(request):
    signup_form = SignupForm(prefix='signup')
    return render(request, 'index/main.html', {'signup_form': signup_form})
