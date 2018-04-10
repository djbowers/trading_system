from .event import Event, EventType


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """

    def __init__(self, symbol_data):
        self.type = EventType.MARKET
        self.symbol_data: dict = symbol_data
