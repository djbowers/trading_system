import unittest
import os

from trading_system.config import TestingConfig


class TestDataDir(unittest.TestCase):

    def setUp(self):
        config = TestingConfig()
        price_data_dir = config.price_dir
        csv_path_template = os.path.join(price_data_dir, '{}.csv')
        symbols = config.SYMBOLS
        self.csv_files = {symbol: csv_path_template.format(symbol) for symbol in symbols}

    def test_csv_files_exist_for_each_symbol(self):
        for symbol, csv_file in self.csv_files.items():
            self.assertTrue(os.path.exists(csv_file), "The {}.csv file no longer exists.".format(symbol))


if __name__ == '__main__':
    unittest.main()

