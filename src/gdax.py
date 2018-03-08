from datetime import datetime, timedelta
from time import sleep

import pandas
import requests


class GDAX(object):
    """Class for fetching candle data for a given currency pair."""

    def __init__(self, pair: str):
        """
        Create the exchange object.

        :param pair: Currency pair (e.g., 'BTC-USD', 'ETH-USD'...)
        """
        self.pair = pair
        self.uri = 'https://api.gdax.com/products/{pair}/candles'.format(pair=self.pair)

    def fetch(self, start: datetime, end: datetime, granularity: int) -> pandas.DataFrame:
        """
        Fetch the candle data for a given range and granularity.

        :param start: The start of the date range
        :param end: The end of the date range (excluded)
        :param granularity: The granularity of the candle data (in minutes)
        :return: A data frame of the OHLC and volume information, indexed by their unix timestamp
        """
        data = []
        window_size = 300  # GDAX has limit of returning maximum of 350 items per request

        delta = timedelta(minutes=granularity * window_size)

        slice_start = start
        while slice_start != end:
            slice_end = min(slice_start + delta, end)
            data += self.request_slice(slice_start, slice_end, granularity)
            slice_start = slice_end

        data_frame = pandas.DataFrame(data=data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        data_frame.set_index('time', inplace=True)
        return data_frame

    def request_slice(self, start, end, granularity):
        retries = 3  # Allow 3 retries (we might get rate limited)

        for retry_count in range(0, retries):
            # From https://docs.gdax.com/#get-historic-rates the response is in the format:
            # [[time, low, high, open, close, volume], ...]
            response = requests.get(self.uri, {
                'start': GDAX._date_to_iso8601(start),
                'end': GDAX._date_to_iso8601(end),
                'granularity': granularity * 60  # GDAX API granularity is in seconds.
            })

            if response.status_code != 200 or not len(response.json()):
                if retry_count + 1 == retries:
                    raise Exception('Failed to get exchange data for ({}, {})!'.format(start, end))
                else:
                    # Exponential back-off.
                    sleep(1.5 ** retry_count)
            else:
                # Sort the historic rates (in ascending order) based on the timestamp.
                result = sorted(response.json(), key=lambda x: x[0])
                return result

    @staticmethod
    def _date_to_iso8601(date: datetime) -> str:
        """
        Convert a datetime object to the ISO-8601 date format (expected by the GDAX API).

        :param date: The date to be converted
        :return: The ISO-8601 formatted date
        """
        return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour,
            minute=date.minute,
            second=date.second)
