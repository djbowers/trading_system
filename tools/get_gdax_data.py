#!/usr/bin/env python

from datetime import datetime

from src.gdax import GDAX


def btc_usd_60min(start, end):
    return GDAX('BTC-USD').fetch(start, end, 60)


if __name__ == "__main__":
    data_frame = btc_usd_60min(datetime(2018, 3, 1, 0), datetime(2018, 3, 20, 0))
    print(data_frame)

    # Save to CSV
    data_frame.to_csv('../data/data.csv')
