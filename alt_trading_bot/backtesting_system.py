#!/usr/bin/env python

import queue
import time


class TradingSystem:
    """
    The TradingSystem class represents the actual trading system itself. It stores
    all of the modules it needs to run as instance variables.
    """
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def run(self):
        while True:
            # Update the bars (specific backtest code, as opposed to live trading)
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break

            self.handle_events()
            self.ten_minute_heartbeat()

    def handle_events(self):
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

    def ten_minute_heartbeat(self):
        """
        Wait for 10 minutes for proceeding.
        """
        time.sleep(10 * 60)


if __name__ == '__main__':
    TradingSystem().run()
