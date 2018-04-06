from .event import Event


class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """

    def __init__(self, symbol, datetime, signal_type):
        """
        symbol: The ticker symbol, e.g. 'BTC'.
        datetime: The timestamp at which the signal was generated.
        signal_type: 'LONG' or 'SHORT'
        """

        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
