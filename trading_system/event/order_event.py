from .event import Event, EventType


class OrderEvent(Event):
    """
    Handles the event of sending an order to an execution system.
    """

    def __init__(self, symbol: str, order_type: str, quantity: float, direction: str):
        """
        symbol: The instrument to trade (e.g. 'BTC')
        order_type: 'MKT' or 'LMT' for Market or Limit
        quantity: Non-negative float for quantity
        direction: 'BUY' or 'SELL' for long or short
        """

        self.type = EventType.ORDER
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
