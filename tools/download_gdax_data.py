import os
from datetime import datetime

from config import PRICE_DATA_LOCATION
from trading_system.gdax import GDAX

SYMBOL = 'LTC'


def download_data():
    start = datetime(2018, 3, 1, 0)
    end = datetime(2018, 3, 2, 0)
    granularity = 60

    data_frame = get_data_frame(start, end, granularity)
    save_to_csv(data_frame)


def get_data_frame(start, end, granularity):
    return GDAX('{}-USD'.format(SYMBOL)).fetch(start, end, granularity)


def save_to_csv(data_frame):
    if not os.path.exists(PRICE_DATA_LOCATION):
        os.mkdir(PRICE_DATA_LOCATION)
    data_frame.to_csv(os.path.join(PRICE_DATA_LOCATION, '{}.csv'.format(SYMBOL)))


if __name__ == "__main__":
    download_data()
