class NaivePortfolio:
    """
    The Portfolio data structure contains all of the financial portfolio data
    for the current trading session.

    The current positions and current holdings represent data for the most recent
    market information. The all positions and all holdings represent snapshots of
    the portfolio at a point in time specified by the datetime.
    """

    def __init__(self, symbols, start_date, initial_capital=100000.0):
        self.start_date = start_date
        self.initial_capital = initial_capital

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
