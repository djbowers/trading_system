import os
from datetime import datetime

from alt_trading_bot.gdax.currency_pair import CurrencyPair
from config import base_path


def get_data_frame(start, end, granularity):
    return CurrencyPair('BTC-USD').fetch(start, end, granularity)


def save_to_csv(data_frame):
    data_frame.to_csv(os.path.join(base_path, 'data/data.csv'))


def run():
    start = datetime(2018, 3, 1, 0)
    end = datetime(2018, 3, 2, 0)
    granularity = 60

    data_frame = get_data_frame(start, end, granularity)
    save_to_csv(data_frame)


if __name__ == "__main__":
    run()
