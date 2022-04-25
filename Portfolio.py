from Index import Index

class Portfolio:
    def __init__(self, initial_balance: int, index: Index):
        self.initial_balance = initial_balance
        self.index = index
        self.bag = {}

        self.current_balance = initial_balance
    
    # def UpdatePortfolio(self):
    #     self.current_balance -= self.current_balance*0.001
    #     for symbol, weight in self.index.symbols_weights.items():
    #         pass