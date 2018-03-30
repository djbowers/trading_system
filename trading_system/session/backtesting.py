import queue
import time

from trading_system.event import EventType
from .base import BaseTradingSession


class BacktestingSession(BaseTradingSession):
    """
    Represents a simulated trading session used for backtesting.
    """
    def __init__(self, data_handler, event_queue, strategy, portfolio, execution_handler):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution_handler = execution_handler

    def run(self):
        while True:
            # Update the bars (specific backtest code, as opposed to live trading)
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break

            self.handle_events()
            self.wait_for_update(1)

    def handle_events(self):
        """
        Inner event-loop that actually handles the events from the
        EventQueue object. Specific events are delegated to
        their respective component and subsequently new events are
        added to the queue. When the event queue is empty, the
        heartbeat loop continues.
        """
        while True:
            try:
                event = self.event_queue.get(False)
            except queue.Empty:
                break
            else:
                if event is not None:
                    if event.type == EventType.MARKET:
                        self.strategy.calculate_signals(event)
                        self.portfolio.update_timeindex(event)

                    elif event.type == EventType.SIGNAL:
                        self.portfolio.update_signal(event)

                    elif event.type == EventType.ORDER:
                        self.execution_handler.execute_order(event)

                    elif event.type == EventType.FILL:
                        self.portfolio.update_fill(event)

    @staticmethod
    def wait_for_update(wait_time):
        """
        Wait a specified amount of time before the next update, where wait_time
        is in minutes.
        """
        time.sleep(wait_time * 60)
