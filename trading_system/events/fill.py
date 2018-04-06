from .event import Event


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from an exchange or brokerage. Stores the quantity of an instrument
    actually filled and at what price.
    """

    def __init__(self, timeindex, symbol, quantity,
                 direction, fill_cost, exchange, fee=0.0):
        """
        timeindex: The bar-resolution when the order was filled
        symbol: The instrument which was filled
        quantity: The filled quantity
        direction: The direction of fill ('BUY' or 'SELL')
        fill_cost: The holdings value in dollars
        exchange: The exchange where the order was filled
        fee: The exchange fee
        """

        self.timeindex = timeindex
        self.symbol = symbol
        self.quantity = quantity
        self._direction = direction
        self.fill_cost = fill_cost
        self.exchange = exchange
        self.fee = fee

    @property
    def fill_dir(self):
        if self._direction == 'BUY':
            return 1
        elif self._direction == 'SELL':
            return -1
        else:
            raise ValueError("The event direction was set as something other than BUY or SELL.")
