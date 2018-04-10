import pandas as pd

from trading_system.event import OrderEvent, SignalEvent, FillEvent, EventQueue, MarketEvent
from trading_system.performance import create_drawdowns, create_sharpe_returns
from .portfolio_handler import PortfolioHandler


class NaivePortfolioHandler(PortfolioHandler):
    """
    The NaivePortfolio object is designed to send orders to
    an exchange object with a constant quantity size blindly,
    i.e. without any risk management or position sizing. It is
    used to test simpler strategies such as BuyAndHoldStrategy.
    """

    def __init__(self, events: EventQueue, symbols, start_date, initial_capital=100000.0):
        """
        Initialises the portfolio with a price handler and an event queue.
        Also includes a starting datetime index and initial capital
        (USD unless otherwise stated).
        """
        self.events = events
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.equity_curve = None

        self.current_positions = {symbol: 0 for symbol in symbols}

        self.all_positions = [
            dict(self.current_positions, **{'datetime': self.start_date})
        ]

        self.current_holdings = dict({symbol: 0.0 for symbol in symbols},
                                     **{'cash': self.initial_capital,
                                        'fees': 0.0,
                                        'total': self.initial_capital})

        self.all_holdings = [
            dict(self.current_holdings, **{'datetime': self.start_date})
        ]

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
        symbol = list(event.symbol_data.keys())[0]
        bars = event.symbol_data[symbol]
        timeindex = bars[0].time

        self._update_all_positions(event.symbol_data, timeindex)
        self._update_all_holdings(event.symbol_data, timeindex)

    def create_equity_curve(self):
        """
        Creates a pandas DataFrame from the all_holdings list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0+curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self):
        """
        Creates a list of summary statistics for the portfolio such as
        Sharpe Ratio and drawdown information.
        """
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']

        sharpe_ratio = create_sharpe_returns(returns)
        max_dd, dd_duration = create_drawdowns(pnl)

        stats = [("Total Return", "%0.2f%%" % ((total_return - 1.0) * 100.0)),
                 ("Sharpe Ratio", "%0.2f" % sharpe_ratio),
                 ("Max Drawdown", "%0.2f%%" % (max_dd * 100.0)),
                 ("Drawdown Duration", "%d" % dd_duration)]
        return stats

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

    def _update_all_positions(self, symbol_data, timeindex):
        new_positions = {'datetime': timeindex}
        for symbol in symbol_data.keys():
            new_positions[symbol] = self.current_positions[symbol]
        self.all_positions.append(new_positions)

    def _update_all_holdings(self, symbol_data, timeindex):
        """
        Updates holdings using the close price of the bar as the current market value.
        """
        newest_holdings = {'datetime': timeindex, 'cash': self.current_holdings['cash'],
                           'fees': self.current_holdings['fees'],
                           'total': self.current_holdings['total']}

        for symbol in symbol_data.keys():
            bars = symbol_data[symbol]
            market_value = self.current_positions[symbol] * bars[0].close
            newest_holdings[symbol] = market_value
            newest_holdings['total'] += market_value

        self.all_holdings.append(newest_holdings)
