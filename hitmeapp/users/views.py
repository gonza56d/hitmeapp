"""Users views."""

# Django
from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _

# Project
from .forms import SignupForm, LoginForm
from . import services


class SignupView(FormView):
    """Handle the index view on GET requests and has the capability to process
    the signup form requests in order to sign up new users on POST.
    """

    template_name = 'index/main.html'
    form_class = SignupForm
    success_url = '/users/signup/'

    def form_valid(self, form: SignupForm) -> HttpResponse:
        """Handle users' signup request via POST method.

        Parameters
        ----------
        form : SignupForm
            Form class used to present the required signup data.
        
        Return
        ------
        HttpResponse : Redirect to index again with the proper notification
            showing success/error on signup.
        """
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
