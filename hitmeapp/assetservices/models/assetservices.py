"""Current asset services to track."""

# Python
from enum import Enum
from typing import List

# Django
from django.urls import reverse


class AssetService:
    """Asset service model to display list in app sidebar
    """

    class Status(Enum):
        AVAILABLE = 'Available'
        MAINTENANCE = 'Under Maintenance'
        COMMIN_SOON = 'Comming Soon!'

    def __init__(self, name: str, url: str, status: Status) -> None:
        """Initialize a new asset service model to display list in app sidebar.

        Parameters
        ----------
        name : str
            Name of the asset service to display to the users.
        
        url : str
            URL to redirect users to the desired asset service view to track.
        
        status : Status
            Enum to set the current status of the asset service. Indicate if
            the asset service is available to use, under mainteinance or
            comming soon (in development).
        """
        self.name = name
        self.url = url
        self.status = status


def get_services_list() -> List[AssetService]:
    """Get the current asset services in AssetService model instances.

    Return
    ------
    list[AssetServices] : n intances with the current asset services witht their
        proper attributes set.
    """
    return [
        AssetService(
            name='Crypto Currency',
            url=str(reverse('assetservices:crypto')),
            status=AssetService.Status.AVAILABLE
        ),
        AssetService(
            name='Mercado Libre',
            url='#',
            status=AssetService.Status.COMMIN_SOON
        ),
        AssetService(
            name='Amazon',
            url='#',
            status=AssetService.Status.COMMIN_SOON
        ),
    ]
