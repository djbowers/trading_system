class PriceBar:
    def __init__(self, time_index, open_price, low_price, high_price, close_price, volume, symbol):
        self.time = time_index
        self.open = open_price
        self.low = low_price
        self.high = high_price
        self.close = close_price
        self.volume = volume
        self.symbol = symbol
