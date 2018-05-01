from .event import Event, EventType


class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """

    def __init__(self, symbol, datetime, direction):
        """
        symbol: The ticker symbol, e.g. 'BTC'.
        datetime: The timestamp at which the signal was generated.
        signal_type: 'LONG' or 'SHORT'
        """

        self.type = EventType.SIGNAL
        self.symbol = symbol
        self.datetime = datetime
        self.direction = direction
