import time

from trading_system.events import SignalEvent, FillEvent, MarketEvent, OrderEvent, EventQueue
from .engine import Engine
from trading_system.strategy import Strategy
from trading_system.execution import ExecutionHandler

class BacktestingEngine(Engine):
    """
    Represents a simulated trading session used for backtesting.
    """
    def __init__(self, data_handler, events: EventQueue, strategy, portfolio_handler, execution_handler):
        self.data_handler = data_handler
        self.events = events
        self.strategy = strategy
        self.portfolio_handler = portfolio_handler
        self.execution_handler = execution_handler

    def start(self):
        while True:
            # Update the bars (specific backtest code, as opposed to live trading)
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break

            self._handle_events()
            self._wait_for_update()

    def _handle_events(self):
        """
        Inner event-loop that actually handles the events from the
        EventQueue object. Specific events are delegated to
        their respective component and subsequently new events are
        added to the queue. When the event queue is empty, the
        heartbeat loop continues.
        """
        while True:
            event = self.events.maybe_get_next_event()
            if event:
                if isinstance(event, MarketEvent):
                    self.strategy.calculate_signals(event)
                    self.portfolio_handler.update_timeindex(event)

                elif isinstance(event, SignalEvent):
                    self.portfolio_handler.update_signal(event)

                elif isinstance(event, OrderEvent):
                    self.execution_handler.execute_order(event)

                elif isinstance(event, FillEvent):
                    self.portfolio_handler.update_fill(event)
            else:
                break

    @staticmethod
    def _wait_for_update(wait_time=0):
        """
        Wait a specified amount of time before the next update, where wait_time
        is in seconds and defaults to 0.
        """
        time.sleep(wait_time)
