from .event import Event


class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """

    def __init__(self, symbol, order_type, quantity, direction):
        """
        symbol: The instrument to trade
        order_type: 'MKT' or 'LMT' for Market or Limit
        quantity: Non-negative integer for quantity
        direction: 'BUY' or 'SELL' for long or short
        """

        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
