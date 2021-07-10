"""Utility generic functions."""

# Django
from django.forms.utils import ErrorDict


def form_errors_into_string(form_erros: ErrorDict) -> str:
    """Convert form errors dict into human readable message.
    
    Parameters
    ----------
    form_errors : ErrorDict
        Django ErrorDict class with all the current form errors.
    
    Return
    ------
    str : CSV string with each error.
    """
    errors = ''
    for error in form_erros:
        if errors:
            errors = errors + ', '
        errors = errors + form_erros[error][0].lower()
    return errors


def currency_to_float(currency: str) -> float:
    return currency.replace('$', '').replace(',', '').replace('%', '')
