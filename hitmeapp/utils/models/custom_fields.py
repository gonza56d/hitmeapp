"""Project custom fields."""

# Django
from django.db.models import DecimalField


class CurrencyField(DecimalField):
    """Extends from DecimalField with common default settings used in the
    project for fields that pretend to express some currency value.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(max_digits=30, decimal_places=8)
