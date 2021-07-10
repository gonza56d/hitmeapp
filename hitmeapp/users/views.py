"""Users views."""

# Django
from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.utils.translation import gettext as _

# Project
from .forms import SignupForm, LoginForm
from . import services


class SignupView(View):
    """Handle the signup form requests in order to sign up new users on POST.
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle users' signup request.

        Parameters
        ----------
        request : HttpRequest
            Django request object.
        
        Return
        ------
        HttpResponse : Redirect to index again with the proper notification
            showing success/error on signup.
        """
        form = SignupForm(data=request.POST, prefix='signup')
        if form.is_valid():
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
        return redirect('index:main')


class LoginView(View):
    """Handle authentication views for users. Perform login on POST and
    logout on GET.
    """

    form_class = LoginForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle users' logout request via GET method.

        Parameters
        ----------
        request : HttpRequest
            Django request object.
        
        Return
        ------
        HttpResponse : Redirect to app's index with the notification that
            the user has logged out only if user was authenticated before the
            logout request.
        """
        if request.user.is_authenticated:
            services.logout_user(request=request)
            messages.success(request, _('You are logged out'))
        return redirect('index:main')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle users' login request via POST method.

        Parameters
        ----------
        request : HttpRequest
            Django request object.
        
        Return
        ------
        HttpResponse : redirect to app's index with the proper notification
            message regarding login was successful or not.
        """
        form = self.form_class(data=request.POST, prefix='login')
        if form.is_valid():
            user = services.login_user(
                request=request,
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                messages.success(request, _('You are logged in'))
            else:
                messages.warning(request, _('Wrong credentials'))
        return redirect('index:main')
