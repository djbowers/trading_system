from . import EventType
from .base import BaseEvent


class SignalEvent(BaseEvent):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """

    def __init__(self, symbol, datetime, signal_type):
        """
        Initializes the SignalEvent.

        Args:
            symbol: The ticker symbol, e.g. 'GOOG'.
            datetime: The timestamp at which the signal was generated.
            signal_type: 'LONG' or 'SHORT'
        """

        self.type = EventType.SIGNAL
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
