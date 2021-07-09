# Django
from django.core.validators import RegexValidator


class CommonRegex:
    """Common validation regular expressions."""

    LOWERCASE_AND_NUMBERS = RegexValidator(
        regex='[a0-z9]',
        message='Only lowercase letters and numbers allowed.'
    )
    LETTERS_AND_NUMBERS = RegexValidator(
        regex='[aA0-zA9]',
        message='Only letters and numbers allowed.'
    )
    LETTERS = RegexValidator(
        regex='[aA-zZ]',
        message='Only letters allowed.'
    )
    LOWERCASE = RegexValidator(
        regex='[a-z]',
        message='Only lowercase letters allowed.'
    )
