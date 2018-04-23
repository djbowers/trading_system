from trading_system.data import GDAXCSVDataHandler
from trading_system.event import EventQueue, EventType, EmptyQueueException
from trading_system.execution import ExecutionHandler
from trading_system.portfolio import PortfolioHandler
from trading_system.report import ReportHandler
from trading_system.strategy import Strategy
from .engine import Engine


class BacktestingEngine(Engine):
    """
    Represents a simulated trading session used for backtesting.
    """
    def __init__(self, events: EventQueue, data_handler: GDAXCSVDataHandler, strategy: Strategy,
                 portfolio_handler: PortfolioHandler, execution_handler: ExecutionHandler,
                 report_handler: ReportHandler):
        self.data_handler = data_handler
        self.events = events
        self.strategy = strategy
        self.portfolio_handler = portfolio_handler
        self.execution_handler = execution_handler
        self.report_handler = report_handler

    def run(self):
        self._run_backtesting_session()
        self._report_results()

    def _run_backtesting_session(self):
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
            self.portfolio_handler.update_portfolio_on_market(event)

        elif event.type == EventType.SIGNAL:
            self.portfolio_handler.generate_order_from_signal(event)

        elif event.type == EventType.ORDER:
            self.execution_handler.execute_order(event)

        elif event.type == EventType.FILL:
            self.portfolio_handler.update_portfolio_on_fill(event)

    def _report_results(self):
        print(self.report_handler.generate_report())
