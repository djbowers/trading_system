import unittest

from trading_system import data
from trading_system.events import EventQueue
from config import TestingConfig


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.data_handler = data.GDAXCSVDataHandler(EventQueue(),
                                                    TestingConfig.DATA_DIR,
                                                    TestingConfig.SYMBOLS)

    def test_get_latest_bars(self):
        bars = self.data_handler.get_latest_bars('BTC')


    # def test_update_bars(self):
    #     self.data_handler.update_bars()
    #     raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
