from trading_system.event import SignalEvent, MarketEvent, EventQueue
from .strategy import Strategy


class PeriodBreakoutStrategy(Strategy):
    """
    Simply determines if period_high -or- period_low == NOW

    If the period_high -or- period_low == NOW, Returns with long or
    short buy signal.

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


        for symbol, bars in event.symbol_data.items():
            ## get period high
            ## high will be TRUE or FALSE
            high = get_period_high(bars)

            ## get period low
            ## low will be TRUE or FALSE
            low = get_period_low(bars)

            if high == True:
                ## breakout has occured, now == test_period high
                ## create a long buy event
                signal = SignalEvent(symbol, bars[-1].time, 'LONG')
                self.events.add_event(signal)
                self.bought[symbol] = True

            if low == True:
                ## breakout has occured, now == test_period high
                ## create a short buy event
                signal = SignalEvent(symbol, bars[-1].time, 'SHORT')
                self.events.add_event(signal)
                self.bought[symbol] = True



    def get_period_high(self):
        """
        Run through the data given and determine if the highest close amount
        is equal to the last candle's 'time' (in dict)

        Last candle == now
        """

        ## set results to 0
        results = False
        highest_price_in_dict = {'time':0,
                                'price':0}
        """
        loop 1 candle at a time and compare if current close price is higher
        than last close price. End the loop with the highest close price as
        a dict with the period.
        """
        for bar in bars:
            if bar.close_price > highest_price_in_dict['price']:
                highest_price_in_dict = {'time':bar.time_index,
                                'price':bar.close_price}

            now = bar

        """
        after looping throught he candles, the highest price with its time
        will be in highest_price_in_dict. If highest_price_in_dict['time'] ==
        last_record['time'], period_high == True (go long).
        """
        if highest_price_in_dict['time'] == now.time_index:
            results = True


        return results


    def get_period_low(self):
        """
        Run through the data given and determine if the highest close amount
        is equal to the last candle's 'time' (in dict)

        Last candle == now
        """

        ## set results to 0
        results = [False, '']
        lowest_price_in_dict = {'time':0,
                                'price':9999999999999}

        """
        loop 1 candle at a time and compare if current close price is higher
        than last close price. End the loop with the highest close price as
        a dict with the period.
        """
        if bar.close_price < lowest_price_in_dict['price']:
            lowest_price_in_dict = {'time':bar.time_index,
                            'price':bar.close_price}
        now = bar


        """
        after looping throught he candles, the highest price with its time
        will be in highest_price_in_dict. If highest_price_in_dict['time'] ==
        last_record['time'], period_high == True (go long).
        """
        if lowest_price_in_dict['time'] == bar.time_index:
            results = True


        return results
