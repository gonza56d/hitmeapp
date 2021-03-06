"""Users views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.utils.translation import gettext_lazy as _

# Project
from .forms import SignupForm, LoginForm
from . import services
from hitmeapp.assetservices.models import CryptoTracking
from hitmeapp.utils.exceptions import BusinessException
from hitmeapp.utils.generic_functions import form_errors_into_string


class MyProfile(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle users' request to see their own profile data.

        Parameters
        ----------
        request : HttpRequest
            Django request object.
        
        Return
        ------
        HttpResponse : Display the proper template with all the user in session data.
        """
        crypto_trackings = CryptoTracking.objects.filter(user=request.user)
        return render(request, 'users/my_profile.html', {'crypto_trackings': crypto_trackings})


class SignupView(View):
    """Handle the signup form requests in order to sign up new users on POST.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
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
        try:
            if form.is_valid(): # TRY to create a new user if form is valid
                services.create_user(
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password'),
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    phone_number=form.cleaned_data.get('phone_number')
                )
                messages.success(self.request, _('Account created successfully'))
            else: # Show form errors in warning notification if form is not valid
                errors = form_errors_into_string(form.errors)
                messages.warning(request, errors)
        except BusinessException as e: # Notify that email is already in use if business exception
            messages.error(self.request, _(str(e)))
        finally:
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
