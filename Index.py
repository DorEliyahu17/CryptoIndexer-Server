from pandas import Timestamp
from DataUtils import GetHistoricalPriceData


class Index:
    def __init__(self, name: str = '', creator: str = ''):
        self.name = name
        self.creator = creator
        self.symbols_weights = {}

    def AddSymbol(self, symbol: str, weight: float):
        if symbol in self.symbols_weights.keys():
            return
        sum_w = sum(self.symbols_weights.values())
        if sum_w >= 1:
            return
        self.symbols_weights[symbol] = min(1-sum_w, weight)

    def RemoveSymbol(self, symbol: str):
        self.symbols_weights.pop(symbol, None)

    def UpdateWeight(self, symbol: str, weight: float):
        self.RemoveSymbol(symbol)
        self.AddSymbol(symbol, weight)

    def Backtest(self, initial_balance: int, fees: float) -> tuple[list[Timestamp], list[float]]:
        symbols_prices = {}
        for symbol in self.symbols_weights.keys():
            symbols_prices[symbol] = GetHistoricalPriceData(
                symbol)[['Close', 'Close time']]

        min_len = min([len(prices) for prices in symbols_prices.values()])
        dates = list(symbols_prices.values())[0]['Close time'].tail(
            min_len).reset_index(drop=True)
        for symbol, price in symbols_prices.items():
            symbols_prices[symbol] = price['Close'].tail(
                min_len).reset_index(drop=True)

        def Buy(balance: float, i: int) -> dict:
            bag = {}
            balance -= balance*fees
            for symbol, weight in self.symbols_weights.items():
                bag[symbol] = balance*weight/symbols_prices[symbol][i]
            return bag

        def Sell(bag: dict, i: int) -> float:
            balance = 0
            for symbol in bag.keys():
                balance += bag[symbol]*symbols_prices[symbol][i]
            balance -= balance*fees
            return balance

        balance_progress = [initial_balance]
        bag = Buy(initial_balance, 0)
        for i in range(1, min_len):
            balance = Sell(bag, i)
            balance_progress.append(balance)
            bag = Buy(balance, i)

        if len(dates) != len(balance_progress):
            raise Exception(
                'Problem with backtesting, length of dates array does not match the length of the balance progress.')

        return list(dates), balance_progress
