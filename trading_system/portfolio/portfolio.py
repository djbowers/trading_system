class Portfolio:
    def __init__(self, symbols, start_date, initial_capital=100000.0):
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.equity_curve = None

        self.current_positions = {symbol: 0 for symbol in symbols}

        self.all_positions = [
            dict(self.current_positions, **{'datetime': self.start_date})
        ]

        self.current_holdings = dict({symbol: 0.0 for symbol in symbols},
                                     **{'cash': self.initial_capital,
                                        'fees': 0.0,
                                        'total': self.initial_capital})

        self.all_holdings = [
            dict(self.current_holdings, **{'datetime': self.start_date})
        ]
