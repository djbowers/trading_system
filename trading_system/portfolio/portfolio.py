from pandas import DataFrame


class Portfolio:

    def __init__(self, symbols, start_date, initial_capital=100000.0):
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.equity_curve: DataFrame = None

        self.current_positions = {symbol: 0 for symbol in symbols}

        self.all_positions = [
            dict({'datetime': self.start_date}, **self.current_positions)
        ]

        self.current_holdings = dict({'cash': self.initial_capital,
                                      'fees': 0.0,
                                      'total': self.initial_capital},
                                     **{symbol: 0.0 for symbol in symbols})

        self.all_holdings = [
            dict({'datetime': self.start_date}, **self.current_holdings)
        ]
