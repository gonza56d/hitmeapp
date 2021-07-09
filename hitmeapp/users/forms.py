"""User forms."""

# Django
from django import forms
from django.forms.widgets import EmailInput, NumberInput, PasswordInput, TextInput
from django.utils.translation import gettext as _


class LoginForm(forms.Form):

    email = forms.CharField(widget=EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    password = forms.CharField(widget=PasswordInput(
        attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password'
        })
    )


class SignupForm(LoginForm):

    first_name = forms.CharField(widget=TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('First name')
        }
    ))

    last_name = forms.CharField(widget=TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Last name')
        }
    ))

    phone_number = forms.CharField(widget=NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Phone number')
        }
    ))
