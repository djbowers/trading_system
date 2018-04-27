from typing import List

from trading_system.event import SignalEvent, FillEvent, EventQueue, MarketEvent, OrderEvent
from .suggested_order import SuggestedOrder
from .position_sizing.position_sizer_mock import PositionSizerMock
from .risk_management.risk_manager_mock import RiskManagerMock
from .portfolio import Portfolio


class PortfolioHandler:
    """
    The PortfolioHandler interacts with the backtesting or live
    trading engine. It exposes two methods, on_signal and
    on_fill, which handle how SignalEvent and FillEvent
    objects are dealt with.

    Each PortfolioHandler contains a Portfolio object,
    which stores the actual Position objects.

    The PortfolioHandler takes a handle to a PositionSizer
    object which determines a mechanism, based on the current
    Portfolio, as to how to size a new Order.

    The PortfolioHandler also takes a handle to the
    RiskManager, which is used to modify any generated
    Orders to remain in line with risk parameters.
    """

    def __init__(self, events: EventQueue, portfolio, position_sizer, risk_manager):
        self._events = events
        self._portfolio: Portfolio = portfolio
        self._position_sizer: PositionSizerMock = position_sizer
        self._risk_manager: RiskManagerMock = risk_manager

    def update_portfolio_on_fill(self, fill: FillEvent):
        """
        Adds a new FillEvent to the Portfolio.
        """
        self._portfolio.add_new_fill(fill)

    def update_portfolio_on_market(self, market: MarketEvent):
        """
        Updates the Portfolio Positions with new market data from a MarketEvent.
        """
        self._portfolio.update_market_value(market)

    def generate_order_from_signal(self, signal: SignalEvent):
        """
        Acts on a SignalEvent to generate new orders based on the portfolio logic.

        Orders are sized by the PositionSizer object and then
        sent to the RiskManager to verify, modify or eliminate.

        Once received from the RiskManager they are converted into
        full OrderEvent objects and sent back to the events queue.
        """
        initial_order = self._suggest_order_from_signal(signal)
        sized_order = self._call_position_sizer(initial_order)
        order_events = self._call_risk_manager(sized_order)
        self._place_orders_onto_queue(order_events)

    @staticmethod
    def _suggest_order_from_signal(signal: SignalEvent):
        """
        Take a SignalEvent object and use it to form a
        SuggestedOrder object. These are not OrderEvent objects,
        as they have yet to be sent to the RiskManager object.
        At this stage they are simply "suggestions" that the
        RiskManager will either verify, modify or eliminate.
        """
        order = SuggestedOrder(
            signal.symbol, signal.direction
        )
        return order

    def _call_position_sizer(self, initial_order: SuggestedOrder):
        """
        Size the quantity of the initial order using the PositionSizer.
        """
        sized_order = self._position_sizer.size_order(
            self._portfolio, initial_order
        )
        return sized_order

    def _call_risk_manager(self, sized_order: SuggestedOrder):
        """
        Refine or eliminate the order using the RiskManager.
        """
        order_events = self._risk_manager.refine_orders(
            self._portfolio, sized_order
        )
        return order_events

    def _place_orders_onto_queue(self, order_list: List[OrderEvent]):
        """
        Once the RiskManager has verified, modified or eliminated
        any order objects, they are placed onto the events queue,
        to ultimately be executed by the ExecutionHandler.
        """
        for order_event in order_list:
            self._events.add_event(order_event)
