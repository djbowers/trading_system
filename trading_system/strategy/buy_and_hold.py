from trading_system.events import SignalEvent, MarketEvent, EventQueue
from .strategy import Strategy


class BuyAndHoldStrategy(Strategy):
    """
    This is an extremely simple strategy that goes LONG all of the
    symbols as soon as a bar is received. It will never exit a position.

    It is primarily used as a testing mechanism for the Strategy class
    as well as a benchmark upon which to compare other strategies.
    """

    def __init__(self, data_handler, events: EventQueue):
        self.data_handler = data_handler
        self.symbols = self.data_handler.symbols
        self.event_queue = events

        # Once buy & hold signal is given, these are set to True
        self.bought = self._calculate_initial_bought()

    def calculate_signals(self, event: MarketEvent):
        """
        For "Buy and Hold" we generate a single signal per symbol
        and then no additional signals. This means we are constantly
        long the market from the date of strategy initialisation.
        """
        for symbol in self.symbols:
            bars = self.data_handler.get_latest_bars(symbol)
            if bars and not self.bought[symbol]:
                # (Symbol, Datetime, Type = LONG, SHORT or EXIT)
                signal = SignalEvent(bars[0][0], bars[0][1], 'LONG')
                self.event_queue.add_event(signal)
                self.bought[symbol] = True

    def _calculate_initial_bought(self):
        """
        Adds keys to the bought dictionary for all symbols and sets them to False.
        """
        bought = {}
        for symbol in self.symbols:
            bought[symbol] = False
        return bought


