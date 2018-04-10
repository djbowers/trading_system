import os
from time import gmtime, strftime
from typing import Dict, List

import pandas as pd

from trading_system.errors import SymbolError
from trading_system.event import MarketEvent, EventQueue
from .data_handler import DataHandler
from .price_bar import PriceBar


class GDAXCSVDataHandler(DataHandler):
    """
    Designed to read CSV files for each requested symbol from disk and
    provide an interface to obtain the "latest" price bar.
    """

    def __init__(self, events: EventQueue, csv_dir, symbols):
        """
        It will be assumed that all csv files are of the form
        'symbol.csv', where symbol is a string in the list.

        latest_symbol_data:
            Formatted Pandas DataFrame constructed one at a time
            from new bars that get formatted and added to it from raw_symbol_data
        """
        self.events = events
        self.csv_dir = csv_dir
        if symbols:
            self.symbols = symbols
        else:
            raise AttributeError("No symbols were found.")

        self.raw_symbol_data: Dict[str: pd.DataFrame] = {}
        self.latest_symbol_data: Dict[str: List[PriceBar]] = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def get_latest_bars(self, symbol, num_bars=1):
        """
        Returns the latest num_bars from latest_symbol_data,
        or (num_bars - k) if less k available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            raise SymbolError("That symbol is not available in the historical data set.")
        else:
            return bars_list[-num_bars:]

    def update_bars(self):
        """
        Pushes the latest price bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        try:
            for symbol in self.symbols:
                bar = next(self._get_new_bar(symbol))
                self.latest_symbol_data[symbol].append(bar)
        except StopIteration:
            self.continue_backtest = False
        else:
            symbol_data = {symbol: self.get_latest_bars(symbol, num_bars=1) for symbol in self.symbols}
            self.events.add_event(MarketEvent(symbol_data))

    def _get_new_bar(self, symbol):
        """
        Returns the latest price bar from the data feed as a tuple of
        (symbol, datetime, low, high, open, close, volume).
        """
        for bar in self.raw_symbol_data[symbol]:
            timeindex = bar[0]
            formatted_timeindex = strftime('%Y-%m-%d %H:%M:%S', gmtime(timeindex))
            bar_data = bar[1]

            yield PriceBar(formatted_timeindex,
                           open_price=bar_data[2], low_price=bar_data[0],
                           high_price=bar_data[1], close_price=bar_data[3],
                           volume=bar_data[4], symbol=symbol)

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        """
        combined_index = None
        for symbol in self.symbols:

            # Load the CSV file, indexed on time.
            csv_file = os.path.join(self.csv_dir, '{}.csv'.format(symbol))
            self.raw_symbol_data[symbol] = pd.read_csv(csv_file, index_col=0)

            # Combine the index to pad forward values.
            if combined_index is None:
                combined_index = self.raw_symbol_data[symbol].index
            else:
                combined_index.union(self.raw_symbol_data[symbol].index)

            # Create key for symbol in latest_symbol_data
            self.latest_symbol_data[symbol] = []

        # Reindex dataframes
        for symbol in self.symbols:
            self.raw_symbol_data[symbol] = self.raw_symbol_data[symbol].reindex(index=combined_index, method='pad').iterrows()
