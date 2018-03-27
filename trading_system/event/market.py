from . import EventType
from .base import BaseEvent


class MarketEvent(BaseEvent):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """

    def __init__(self):
        """
        Initializes the MarketEvent.
        """
        self.type = EventType.MARKET
