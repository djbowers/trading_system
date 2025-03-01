from .event import Event, EventType


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from an exchange or brokerage. Stores the quantity of an instrument
    actually filled and at what price.
    """

    def __init__(self, timeindex, symbol, quantity,
                 direction, price, exchange, fee=0.0):
        """
        timeindex: The bar-resolution when the order was filled
        symbol: The instrument which was filled
        quantity: The filled quantity
        direction: The direction of fill ('BUY' or 'SELL')
        fill_cost: The holdings value in dollars
        exchange: The exchange where the order was filled
        fee: The exchange fee
        """

        self.type = EventType.FILL
        self.timeindex = timeindex
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.price = price
        self.exchange = exchange
        self.fee = fee

    @property
    def polarity(self):
        if self.direction == 'BUY':
            return 1
        elif self.direction == 'SELL':
            return -1
        else:
            raise ValueError("The event direction was set as something other than BUY or SELL.")
