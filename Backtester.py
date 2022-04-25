from Index import Index
from DataFetcher import GetHistoricalPriceData

class Backtester:
    def __init__(self, index: Index, initial_balance: int) -> None:
        self.initial_balance = initial_balance
        self.index = index
        if isinstance(index, Index):
            self.prices = {}