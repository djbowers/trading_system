from trading_system.event import EventQueue, EventType, EmptyQueueException
from .engine import Engine


class BacktestingEngine(Engine):
    """
    Represents a simulated trading session used for backtesting.
    """
    def __init__(self, events: EventQueue, data_handler, strategy, portfolio_handler, execution_handler):
        self.data_handler = data_handler
        self.events = events
        self.strategy = strategy
        self.portfolio_handler = portfolio_handler
        self.execution_handler = execution_handler

    def start(self):
        while self.data_handler.continue_backtest:
            try:
                event = self.events.get_next_event()
            except EmptyQueueException:
                self.data_handler.update_bars()
            else:
                self._handle_event(event)

    def _handle_event(self, event):
        if event.type == EventType.MARKET:
            self.strategy.calculate_signals(event)
            self.portfolio_handler.update_portfolio(event)

        elif event.type == EventType.SIGNAL:
            self.portfolio_handler.update_on_signal(event)

        elif event.type == EventType.ORDER:
            self.execution_handler.execute_order(event)

        elif event.type == EventType.FILL:
            self.portfolio_handler.update_on_fill(event)
