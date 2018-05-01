#!/usr/bin/env python

from config import Config, DevelopmentConfig
from trading_system.data import GDAXCSVDataHandler
from trading_system.engine import BacktestingEngine
from trading_system.event import EventQueue
from trading_system.execution import SimulatedExecutionHandler
from trading_system.portfolio import PortfolioHandler, Portfolio, PositionSizerMock, RiskManagerMock
from trading_system.strategy import BuyAndHoldStrategy
from trading_system.report import ReportHandler


def run(config: Config = DevelopmentConfig()):
    events = EventQueue()
    csv_dir = config.DATA_DIR
    symbols = config.SYMBOLS

    data_handler = GDAXCSVDataHandler(events, symbols, csv_dir)
    strategy = BuyAndHoldStrategy(events, symbols)

    portfolio = Portfolio()
    position_sizer = PositionSizerMock()
    risk_manager = RiskManagerMock()
    portfolio_handler = PortfolioHandler(events, portfolio, position_sizer, risk_manager)

    execution_handler = SimulatedExecutionHandler(events)
    report_handler = ReportHandler(portfolio)

    engine = BacktestingEngine(events, data_handler, strategy, portfolio_handler,
                               execution_handler, report_handler)

    engine.run()


if __name__ == '__main__':
    run()
