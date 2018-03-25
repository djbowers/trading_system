import os
from datetime import datetime

from config import data_dir
from trading_system.gdax import GDAX


def download_data():
    start = datetime(2018, 3, 1, 0)
    end = datetime(2018, 3, 2, 0)
    granularity = 60

    data_frame = get_data_frame(start, end, granularity)
    save_to_csv(data_frame)


def get_data_frame(start, end, granularity):
    return GDAX('BTC-USD').fetch(start, end, granularity)


def save_to_csv(data_frame):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    data_frame.to_csv(os.path.join(data_dir, 'btc.csv'))


if __name__ == "__main__":
    download_data()
