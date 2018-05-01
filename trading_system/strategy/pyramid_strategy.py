from trading_system.event import SignalEvent, MarketEvent, EventQueue
from .strategy import Strategy


class PeriodBreakoutStrategy(Strategy):
    """
    Simply determines if period_high -or- period_low == NOW AND has gone
    beyond 1 N in the favorable direction.

    If the period_high -or- period_low == NOW && Current price is N Greater
    (or lesser) than last entry signal, buy again.

    The bought dictionary is used to keep track of which assets have been
    purchased.
    """

    def __init__(self, events: EventQueue, symbols):
        self.events = events
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



        ## get period high
        high = get_period_high(total_candle_dict)

        ## get period low
        low = get_period_low(total_candle_dict)

        for symbol, bars in event.symbol_data.items():
            if high == True:
                ## breakout has occured, now == test_period high
                ## create a long buy event
                signal = SignalEvent(bars[-1].symbol, bars[-1].time, 'LONG')
                self.events.add_event(signal)
                self.bought[symbol] = True

            if low == True:
                ## breakout has occured, now == test_period high
                ## create a short buy event
                signal = SignalEvent(bars[-1].symbol, bars[-1].time, 'SHORT')
                self.events.add_event(signal)
                self.bought[symbol] = True



    def get_period_high(self):
        """
        See if current price is N higher or lower than buy trigger
        """


        """
        Using N as risk management

        N is calculated the same as ATR and ultimately will be passed in
        by the risk manager
        """
        N = 500


        ## set results to 0
        results = False

        for symbol, bars in event.symbol_data.items():
            now = bars[-1]

        ## Sample for now, should get from reporting
        last_buy_signal = 10111

        """
        if the current close price is higher than the last entry signal
        + N, Buy!
        """
        if now.close_price > (last_buy_signal + N):
            results = True


        return results


    def get_period_low(self):
            """
            See if current price is N higher or lower than buy trigger
            """


            """
            Using N as risk management

            N is calculated the same as ATR and ultimately will be passed in
            by the risk manager
            """
            N = 500


            ## set results to 0
            results = False

            for symbol, bars in event.symbol_data.items():
                now = bars[-1]

            ## Sample for now, should get from reporting
            last_buy_signal = 10111

            """
            if the current close price is higher than the last entry signal
            + N, Buy!
            """
            if now.close_price < (last_buy_signal + N):
                results = True


            return results
