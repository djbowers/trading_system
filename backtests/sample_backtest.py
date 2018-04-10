#!/usr/bin/env python

from datetime import datetime

from config import Config, DevelopmentConfig
from trading_system.data import GDAXCSVDataHandler
from trading_system.engine import BacktestingEngine
from trading_system.event import EventQueue
from trading_system.execution import SimulatedExecutionHandler
from trading_system.portfolio import NaivePortfolioHandler, Portfolio
from trading_system.strategy import BuyAndHoldStrategy


def run(config: Config = DevelopmentConfig()):
    events = EventQueue()
    csv_dir = config.DATA_DIR
    symbols = config.SYMBOLS
    start_date = datetime.utcnow()
    portfolio = Portfolio(symbols, start_date)

    data_handler = GDAXCSVDataHandler(events, symbols, csv_dir)
    strategy = BuyAndHoldStrategy(events, symbols)
    portfolio_handler = NaivePortfolioHandler(events, portfolio)
    execution_handler = SimulatedExecutionHandler(events)

    engine = BacktestingEngine(events, data_handler, strategy, portfolio_handler, execution_handler)

    engine.start()


if __name__ == '__main__':
    run()
