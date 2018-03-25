import unittest
import csv
import os

from . import TEST_DATA_DIR
from .data_validation import SAMPLE1_RAW


class TestDataDir(unittest.TestCase):

    def setUp(self):
        self.sample1_csv_file = os.path.join(TEST_DATA_DIR, 'sample1.csv')

    def test_sample1_csv_file(self):
        try:
            with open(self.sample1_csv_file, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                bars = [row for row in reader]
        except FileNotFoundError:
            bars = []

        self.assertEqual(SAMPLE1_RAW, bars,
                         "The sample1.csv file has been tampered with or no longer exists.")


if __name__ == '__main__':
    unittest.main()

