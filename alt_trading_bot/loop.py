#!/usr/bin/env python

import datetime
import os
import queue
import time

import pytz

from config import base_path
from .data_handler.historic_csv import HistoricCSVDataHandler as DataHandler
from .portfolio.naive import NaivePortfolio as Portfolio
from .strategy.buy_and_hold import BuyAndHoldStrategy as Strategy

# Establish the event queue
events = queue.Queue()
csv_dir = os.path.join(base_path, 'data')
symbol_list = 'BTC'
# start_date = datetime.datetime.now(tz=pytz.timezone('US/Pacific'))

# Declare the components with respective parameters
bars = DataHandler(events, csv_dir, symbol_list)
strategy = Strategy(bars, events)
# port = Portfolio(bars, events, )
# broker = ExecutionHandler(..)


def handle_events():
    """
    Inner event-loop that actually handles the Events from the
    events Queue object. Specific events are delegated to
    the respective component and subsequently new events are
    added to the queue. When the events Queue is empty, the
    heartbeat loop continues
    """
    while True:
        try:
            event = events.get(False)
        except queue.Empty:
            break
        else:
            if event is not None:
                if event.type == 'MARKET':
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type == 'SIGNAL':
                    port.update_signal(event)

                elif event.type == 'ORDER':
                    broker.execute_order(event)

                elif event.type == 'FILL':
                    port.update_fill(event)

def ten_minute_heartbeat():
    """
    Wait for 10 minutes for proceeding.
    """
    time.sleep(10 * 60)

def run():
    while True:
        # Update the bars (specific backtest code, as opposed to live trading)
        if bars.continue_backtest:
            bars.update_bars()
        else:
            break

        handle_events()
        ten_minute_heartbeat()


if __name__ == '__main__':
    run()
