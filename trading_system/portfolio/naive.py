from math import floor

import pandas as pd

from trading_system.event import OrderEvent, EventType
from .base import BasePortfolio


class NaivePortfolio(BasePortfolio):
    """
    The NaivePortfolio object is designed to send orders to
    an exchange object with a constant quantity size blindly,
    i.e. without any risk management or position sizing. It is
    used to test simpler strategies such as BuyAndHoldStrategy.
    """

    def __init__(self, price_handler, event_queue, start_date, initial_capital=100000.0):
        """
        Initialises the portfolio with a price handler and an event queue.
        Also includes a starting datetime index and initial capital
        (USD unless otherwise stated).
        """
        self.price_handler = price_handler
        self.event_queue = event_queue
        self.symbols = self.price_handler.symbols
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.all_positions = self._construct_all_positions()
        self.current_positions = self._construct_positions_list()

        self.all_holdings = self._construct_all_holdings()
        self.current_holdings = self._construct_current_holdings()

    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the portfolio logic.
        """
        if event.type == EventType.SIGNAL:
            order_event = self._generate_naive_order(event)
            self.event_queue.put(order_event)

    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings
        from a FillEvent.
        """
        if event.type == EventType.FILL:
            self._update_positions_from_fill(event)
            self._update_holdings_from_fill(event)

    def update_timeindex(self, event):
        """
        Adds a new record to the positions matrix for the current
        market data bar. This reflects the PREVIOUS bar, i.e. all
        current market data at this stage is known (OLHCVI).

        Makes use of a MarketEvent from the events queue.
        """
        bars = {}
        for s in self.symbols:
            bars[s] = self.price_handler.get_latest_bars(s, num_bars=1)

        # Update positions
        dp = self._construct_positions_list()
        dp['datetime'] = bars[self.symbols[0]][0][1]

        for s in self.symbols:
            dp[s] = self.current_positions[s]

        # Append the current positions
        self.all_positions.append(dp)

        # Update holdings
        dh = self._construct_holdings_list()
        dh['datetime'] = bars[self.symbols[0]][0][1]
        dh['cash'] = self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']

        for s in self.symbols:
            # Approximation to the real value
            market_value = self.current_positions[s] * bars[s][0][5]
            dh[s] = market_value
            dh['total'] += market_value

        # Append the current holdings
        self.all_holdings.append(dh)

    def create_equity_curve_dataframe(self):
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0+curve['returns']).cumprod()
        self.equity_curve = curve

    def _construct_positions_list(self):
        """
        Use dictionary comprehension to create a dictionary for each symbol
        and set the value to zero for each.
        """
        return dict((k, v) for k, v in [(s, 0) for s in self.symbols])

    def _construct_holdings_list(self):
        """
        Use dictionary comprehension to create a dictionary for each symbol
        and set the value to zero for each.
        """
        return dict((k, v) for k, v in [(s, 0.0) for s in self.symbols])

    def _construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        d = self._construct_positions_list()
        d['datetime'] = self.start_date
        return [d]

    def _construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        d = self._construct_holdings_list()
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return [d]

    def _construct_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous
        value of the portfolio across all symbols.
        """
        d = self._construct_holdings_list()
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return d

    def _update_positions_from_fill(self, fill):
        """
        Takes a FillEvent object and updates the position matrix
        to reflect the new position.

        Args:
            fill: The FillEvent object to update the positions with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update positions list with new quantities
        self.current_positions[fill.symbol] += fill_dir*fill.quantity

    def _update_holdings_from_fill(self, fill):
        """
        Takes a FillEvent object and updates the holdings matrix
        to reflect the holdings value.

        Args:
            fill: The FillEvent object to update the holdings with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update the holdings list with new quantities
        fill_cost = self.price_handler.get_latest_bars(fill.symbol)[0][5]  # Close price
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)

    def _generate_naive_order(self, signal):
        """
        Simply transacts an OrderEvent object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Args:
            signal: The SignalEvent signal information.
        """
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength

        mkt_quantity = floor(100*strength)
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        if direction == 'SHORT' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')

        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')
        return order
