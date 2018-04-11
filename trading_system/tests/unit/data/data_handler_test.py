import unittest
from trading_system.data import DataHandler


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.data_handler = DataHandler()

    def test_for_error_on_get_latest_bars(self):
        self.assertRaises(NotImplementedError, self.data_handler.get_latest_bars, '')

    def test_for_error_on_update_bars(self):
        self.assertRaises(NotImplementedError, self.data_handler.update_bars)
