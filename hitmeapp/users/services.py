"""Users business logic."""

# Django
from django.db import transaction

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
