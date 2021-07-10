"""Users views."""

# Django
from django.contrib import messages
from django.http.response import HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse
from django.utils.translation import gettext as _

# Project
from .forms import SignupForm
from . import services


def signup(request):
    print('YEA')


class SignupView(FormView):

    template_name = 'index/main.html'
    form_class = SignupForm
    success_url = reverse('users:signup')

    def form_valid(self, form) -> HttpResponse:
        user = services.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            phone_number=form.cleaned_data.get('phone_number')
        )
        if user is not None:
            messages.success(self.request, _('Account created successfully'))
        else:
            messages.error(self.request, _('An error occurred'))
        return super().form_valid(form)
