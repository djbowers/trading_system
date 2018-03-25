from .base_event import BaseEvent


class OrderEvent(BaseEvent):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """

    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initializes the order type, setting whether it is
        a Market order ('MKT') or a Limit order ('LMT'), has
        a quantity (integral) and its direction ('BUY' or 'SELL').
        Args:
            symbol: The instrument to trade.
            order_type: 'MKT' or 'LMT' for Market or Limit.
            quantity: Non-negative integer for quantity.
            direction: 'BUY' or 'SELL' for long or short.
        """

        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the values within the Order.
        """
        print("Order: Symbol={}, Type={}, Quantity={}, Direction={}".format(
            self.symbol, self.order_type, self.quantity, self.direction))
