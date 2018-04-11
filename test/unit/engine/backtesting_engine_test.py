import unittest
from unittest.mock import Mock

from trading_system import engine
from trading_system.data import DataHandler
from trading_system.event import EventQueue


class TestBacktestingEngine(unittest.TestCase):

    def setUp(self):
        data_handler = DataHandlerMock()
        events = EventQueue()
        strategy = Mock()
        portfolio_handler = Mock()
        execution_handler = Mock()

        self.engine = engine.BacktestingEngine(events, data_handler, strategy,
                                               portfolio_handler, execution_handler)

    def test_engine_starts(self):
        self.engine.start()


class DataHandlerMock(DataHandler):

    def __init__(self):
        self.continue_backtest = True

    def get_latest_bars(self, symbol, num_bars=1):
        pass

    def update_bars(self):
        self.continue_backtest = False
