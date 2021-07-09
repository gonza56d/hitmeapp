"""Index views"""

# Django
from django.shortcuts import render


def index(request):
    print('f')
    return render(request, 'index/main.html', {})
