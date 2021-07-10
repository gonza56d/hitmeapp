"""Users business logic."""

# Django
from django.contrib import auth
from django.db import transaction
from django.http.request import HttpRequest

# Project
from .models import User, Profile


def create_user(email: str, password: str, first_name: str, last_name: str,
                phone_number: int) -> User:
    """Handle logic to create a new user and profile.

    Parameters
    ----------
    email : str
        User email. It must be unique, creation won't success otherwise.

    password : str
        User password. It must contain at least 8 characters.

    first_name : str
        User first name.
    
    last_name : str
        User last name.

    phone_number : int
        User phone number. Not required. Used for option to receive notifications
        via WhatsApp.
    
    Return
    ------
    User : instance of the new user created.
    """
    user = None
    with transaction.atomic():
        user = User.objects.create_user(email=email, password=password)
        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
    return user


def login_user(request: HttpRequest, email: str, password: str) -> User:
    """Handle user login business logic.
    
    Parameters
    ----------
    request : HttpRequest
        Django request object.

    email : str
        User email as login required credential.

    password : str
        User password as login required credential.

    Return
    ------
    User : Instance of the authenticated used or None if wrong credentials.
    """

    user = auth.authenticate(email=email, password=password)
    if user is not None:
        auth.login(request, user)
    return user


def logout_user(request: HttpRequest) -> None:
    """Handle user logout business logic.

    Parameters
    ----------
    request : HttpRequest
        Django request object.
    """
    auth.logout(request)
