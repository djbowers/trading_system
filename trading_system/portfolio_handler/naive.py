from trading_system.events import OrderEvent, SignalEvent, FillEvent, EventQueue, MarketEvent
from .portfolio_handler import PortfolioHandler


class NaivePortfolioHandler(PortfolioHandler):
    """
    The NaivePortfolio object is designed to send orders to
    an exchange object with a constant quantity size blindly,
    i.e. without any risk management or position sizing. It is
    used to test simpler strategies such as BuyAndHoldStrategy.
    """

    def __init__(self, data_handler, events: EventQueue, start_date, initial_capital=100000.0):
        """
        Initialises the portfolio with a price handler and an event queue.
        Also includes a starting datetime index and initial capital
        (USD unless otherwise stated).
        """
        self.data_handler = data_handler
        self.events = events
        self.symbols = self.data_handler.symbols
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.equity_curve = None

        self.all_positions = self._construct_all_positions()
        self.current_positions = self._construct_empty_positions()

        self.all_holdings = self._construct_all_holdings()
        self.current_holdings = self._construct_current_holdings()

    def update_on_signal(self, event: SignalEvent):
        """
        Acts on a SignalEvent to generate new orders based on the portfolio logic.
        """
        order_event = self._generate_naive_order(event)
        self.events.add_event(order_event)

    def update_on_fill(self, event: FillEvent):
        """
        Updates the portfolio current positions and holdings from a FillEvent.
        """
        self._update_current_positions(event)
        self._update_current_holdings(event)

    def update_portfolio(self, event: MarketEvent):
        """
        Adds a new record to the all positions list for the current
        market data bar. This reflects the PREVIOUS bar, i.e. all
        current market data at this stage is known (OLHCVI).
        """
        bars = {}
        for s in self.symbols:
            # TODO: get this info from MarketEvent instead of data_handler
            bars[s] = self.data_handler.get_latest_bars(s, num_bars=1)

        timeindex = self._generate_timeindex(bars)
        self._update_all_positions(timeindex)
        self._update_all_holdings(bars, timeindex)

    def _generate_timeindex(self, bars):
        symbol = self.symbols[0]
        bar = bars[symbol][0]
        bar = next(bar)
        timeindex = bar[1]
        return timeindex

    def _update_all_holdings(self, bars, timeindex):
        newest_holdings = self._construct_empty_holdings()
        newest_holdings['datetime'] = timeindex
        newest_holdings['cash'] = self.current_holdings['cash']
        newest_holdings['fees'] = self.current_holdings['fees']
        newest_holdings['total'] = self.current_holdings['total']
        for s in self.symbols:
            bar = bars[s][0]
            bar = next(bar)
            close_price = bar[5]  # Used as approximation to market value
            market_value = self.current_positions[s] * close_price
            newest_holdings[s] = market_value
            newest_holdings['total'] += market_value
        self.all_holdings.append(newest_holdings)

    def _update_all_positions(self, timeindex):
        newest_positions = self._construct_empty_positions()
        newest_positions['datetime'] = timeindex
        for s in self.symbols:
            newest_positions[s] = self.current_positions[s]
        self.all_positions.append(newest_positions)

    def _generate_naive_order(self, event: SignalEvent):
        """
        Simply transacts an OrderEvent object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.
        """
        order = None

        symbol = event.symbol
        direction = event.signal_type

        mkt_quantity = 100
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

    def _construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        d = self._construct_empty_positions()
        d['datetime'] = self.start_date
        return [d]

    def _construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        d = self._construct_empty_holdings()
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['fees'] = 0.0
        d['total'] = self.initial_capital
        return [d]

    def _construct_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous
        value of the portfolio across all symbols.
        """
        d = self._construct_empty_holdings()
        d['cash'] = self.initial_capital
        d['fees'] = 0.0
        d['total'] = self.initial_capital
        return d

    def _update_current_positions(self, event: FillEvent):
        """
        Takes a FillEvent object and updates the position matrix to reflect the new position.
        """
        self.current_positions[event.symbol] += event.fill_dir * event.quantity

    def _update_current_holdings(self, event: FillEvent):
        """
        Takes a FillEvent object and updates the holdings matrix to reflect the holdings value.
        """
        cost = event.fill_dir * event.fill_cost * event.quantity

        self.current_holdings[event.symbol] += cost
        self.current_holdings['fees'] += event.fee
        self.current_holdings['cash'] -= (cost + event.fee)
        self.current_holdings['total'] -= (cost + event.fee)

    def _construct_empty_positions(self):
        """
        Use dictionary comprehension to create a dictionary for each symbol
        and set the value to zero for each.
        """
        return dict((k, v) for k, v in [(s, 0) for s in self.symbols])

    def _construct_empty_holdings(self):
        """
        Use dictionary comprehension to create a dictionary for each symbol
        and set the value to zero for each.
        """
        return dict((k, v) for k, v in [(s, 0.0) for s in self.symbols])
