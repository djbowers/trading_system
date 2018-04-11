from .event import Event, EventType


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """

    def __init__(self, symbol_data):
        self.type = EventType.MARKET
        self.symbol_data: dict = symbol_data
        self.timeindex = self._get_timeindex()

    def _get_timeindex(self):
        random_bars = list(self.symbol_data.values())[0]
        first_bar = random_bars[0]
        return first_bar.time
