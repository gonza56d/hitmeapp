"""User forms."""

# Django
from django import forms
from django.forms.widgets import EmailInput, PasswordInput, TextInput


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
    )
