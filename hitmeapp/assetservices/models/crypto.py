
class CryptoCurrency:
    """Model to build instances to display in crypto currency views.
    """

    def __init__(self, name: str, price: float=None, last_day: float=None,
                 last_week: float=None, market_cap: float=None, volume: float=None,
                 circulating_supply: str=None, number: int=None) -> None:
        """Initialize a new instance to display in crypto currency views.

        Parameters
        ----------

        name : str
            Name of the crypto currency.
        
        price : float
            Current price.
        
        last_day : float
            Percentage changed in last 24hs.
        
        last_week : float
            Percentage changed in last 7 days.
        
        market_cap : float
            Currency market cap.
        
        volume : float
            Currency market volume.
        
        circulating_supply : str
            Currency market circulating supply.
        
        number : int
            Global ranking position.
        """
        self.number = number
        self.name = name
        self.price = price
        self.last_day = last_day
        self.last_week = last_week
        self.market_cap = market_cap
        self.volume = volume
        self.circulating_supply = circulating_supply
