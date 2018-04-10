from trading_system.event import SignalEvent, MarketEvent, EventQueue
from .strategy import Strategy


class BuyAndHoldStrategy(Strategy):
    """
    This is an extremely simple strategy that goes LONG all of the
    symbols as soon as a bar is received. It will never exit a position.

    It is primarily used as a testing mechanism for the Strategy class
    as well as a benchmark upon which to compare other strategies.

    The bought dictionary is used to keep track of which assets have been
    purchased.
    """

    def __init__(self, events: EventQueue, symbols):
        self.event_queue = events
        self.symbols = symbols
        self.bought = {}
        for symbol in self.symbols:
            self.bought[symbol] = False

    def calculate_signals(self, event: MarketEvent):
        """
        Generate a single signal per symbol and then no additional
        signals. This means we are constantly long the market from
        the date of strategy initialisation.
        """
        for symbol, bars in event.symbol_data.items():
            if not self.bought[symbol]:
                signal = SignalEvent(bars[-1].symbol, bars[-1].time, 'LONG')
                self.event_queue.add_event(signal)
                self.bought[symbol] = True
