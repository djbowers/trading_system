from trading_system.event import EventQueue
from .strategy import Strategy


class TurtleStrategy(Strategy):
    """
    This strategy uses the methods outlined by Richard Dennis in the
    Turtle Trading method.
    """

    def __init__(self, events: EventQueue):
        self.events = events
