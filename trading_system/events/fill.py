from .event import Event


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from an exchange or brokerage. Stores the quantity of an instrument
    actually filled and at what price.
    """

    def __init__(self, timeindex, symbol, exchange, quantity,
                 direction, fill_cost, fee=None):
        """
        timeindex: The bar-resolution when the order was filled
        symbol: The instrument which was filled
        exchange: The exchange where the order was filled
        quantity: The filled quantity
        direction: The direction of fill ('BUY' or 'SELL')
        fill_cost: The holdings value in dollars
        """

        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.fee = fee
