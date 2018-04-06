import unittest
from trading_system import engines
from unittest.mock import Mock
from trading_system.events import EventQueue
from trading_system.data import DataHandler


class TestBacktestingEngine(unittest.TestCase):

    def setUp(self):
        data_handler = DataHandlerMock()
        events = EventQueue()
        strategy = Mock()
        portfolio_handler = Mock()
        execution_handler = Mock()

        self.engine = engines.BacktestingEngine(data_handler, events, strategy,
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


if __name__ == '__main__':
    unittest.main()
