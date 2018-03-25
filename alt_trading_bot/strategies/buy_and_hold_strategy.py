from .base_strategy import BaseStrategy
from ..events import SignalEvent


class BuyAndHoldStrategy(BaseStrategy):
    """
    This is an extremely simple strategy that goes LONG all of the
    symbols as soon as a bar is received. It will never exit a position.

    It is primarily used as a testing mechanism for the Strategy class
    as well as a benchmark upon which to compare other strategies.
    """

    def __init__(self, data_handler, event_queue):
        """
        Initialises the buy and hold strategy.

        Args:
            data_handler: The DataHandler object that provides bar information.
            event_queue: The EventQueue object.
        """
        self.data_handler = data_handler
        self.symbol_list = self.data_handler.symbol_list
        self.event_queue = event_queue

        # Once buy & hold signal is given, these are set to True
        self.bought = self._calculate_initial_bought()

    def calculate_signals(self, event):
        """
        For "Buy and Hold" we generate a single signal per symbol
        and then no additional signals. This means we are constantly
        long the market from the date of strategy initialisation.

        Args:
            event: A MarketEvent object.
        """
        if event.type == 'MARKET':
            for s in self.symbol_list:
                bars = self.data_handler.get_latest_bars(s, N=1)
                if bars is not None and bars != []:
                    if not self.bought[s]:
                        # (Symbol, Datetime, Type = LONG, SHORT or EXIT)
                        signal = SignalEvent(bars[0][0], bars[0][1], 'LONG')
                        self.event_queue.put(signal)
                        self.bought[s] = True

    def _calculate_initial_bought(self):
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to False.
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] = False
        return bought


