# Project
from .models import CryptoCurrency, CryptoTracking
from hitmeapp.users.models import User


def create_crypto_tracking(user: User, crypto_currency: CryptoCurrency, desired_value: float,
        desired_value_type: str, notification_platform: str) -> CryptoTracking:
    """Handle business logic to create a new CryptoTracking instance.

    Parameters
    ----------
    user : User
        User that is trying to create the new CryptoTracking.
    
    crypto_currency : CryptoCurrency
        CryptoCurrency instance that user is trying to track.
    
    desired_value : float
        The threshold amount that user has set to get notified when the actual
        value of the crypto reaches it.
    
    desired_value_type : str
        Indicate wheter the tracked amount is meant to be a percentage change
        or price change. (E.g. 5% more or $5 more).
    
    notification_platform : str
        Indicate where the user wants to receive the notification when the
        threshold is reached.
    """
    crypto = crypto_currency
    CryptoCurrency.objects.set_current_value(crypto)
    crypto_tracking = CryptoTracking(
        user=user,
        crypto_currency=crypto,
        desired_value_type=desired_value_type,
        desired_value=desired_value,
        notification_platform=notification_platform,
        value_when_tracked=crypto.current_value.price
    )
    crypto_tracking.save()
    return crypto_tracking
