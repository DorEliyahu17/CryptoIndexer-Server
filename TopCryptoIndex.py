from Index import Index
from dataclasses import dataclass
import pandas as pd
import datetime
from DataUtils import earliest_top_market_date, GetTopMarketData

@dataclass
class Asset:
    symbol: str
    weight: float
    curr_price: float
    amount: float=0

class TopCryptoIndex(Index):
    def __init__(self, top_num: int, max_weight: float=1, split_remain_relative: bool=True):
        super().__init__(f'Top {top_num} Crypto Index', 'admin')
        self.__top_num = min(top_num, 10)
        self.__max_weight = max(1/top_num, max_weight)
        self.CalcWeight = self.CalcWeightsSplitRemainRelative if split_remain_relative else self.CalcWeightsSplitRemainEven
    
    def UpdateTopIndex(self, df: pd.DataFrame) -> list[Asset]:
        return self.CalcWeight(df)

    def AddSymbol(self, symbol: str, weight: float):
        pass

    def RemoveSymbol(self, symbol: str):
        pass
    
    def CalcWeightsSplitRemainEven(self, df: pd.DataFrame) -> list[Asset]:
        total_market_cap = df['Market Cap'].head(self.__top_num).sum()
        num = self.__top_num
        reserve = 0
        assets = []
        for i in range(self.__top_num):
            reserve /= num
            x = df['Market Cap'][i]/total_market_cap + reserve

            weight = 0

            if x > self.__max_weight:
                weight = self.__max_weight
                reserve += x - self.__max_weight
            else:
                weight = x
            
            num -= 1
            assets.append(Asset(df['Symbol'][i], weight, df['Price'][i]))
        return assets

    def CalcWeightsSplitRemainRelative(self, df: pd.DataFrame) -> list[Asset]:
        total_market_cap = df['Market Cap'].head(self.__top_num).sum()
        reserve = 0
        reserve_mc = total_market_cap
        assets = []
        for i in range(self.__top_num):
            x = df['Market Cap'][i]/total_market_cap + reserve*df['Market Cap'][i]/reserve_mc
            reserve *= (reserve_mc - df['Market Cap'][i])/reserve_mc
            
            weight = 0

            if x > self.__max_weight:
                weight = self.__max_weight
                reserve += x - self.__max_weight
            else:
                weight = x
            
            reserve_mc -= df['Market Cap'][i]
            assets.append(Asset(df['Symbol'][i], weight, df['Price'][i]))
        return assets

    def Backtest(self, initial_balance: int, fees: float) -> list[float]:
        date = earliest_top_market_date
        
        
        def Buy(balance: float, df: pd.DataFrame) -> list[Asset]:
            assets = self.CalcWeightsSplitRemainRelative(df)
            balance -= balance*fees
            for asset in assets:
                asset.amount = balance*asset.weight/asset.curr_price
            return assets

        def Sell(assets: list[Asset], df: pd.DataFrame) -> float:
            balance = 0
            for asset in assets:
                try:
                    balance += asset.amount*df[df['Symbol'] == asset.symbol]['Price'].iloc[0]
                except:
                    raise Exception(asset.symbol, date)
            balance -= balance*fees
            return balance
        
        df = GetTopMarketData(date)
        balance_progress = [initial_balance]
        assets = Buy(initial_balance, df)
        date += datetime.timedelta(days=7)
        while date <= datetime.date.today():
            df = GetTopMarketData(date)
            if df is not None:
                balance = Sell(assets, df)
                balance_progress.append(balance)
                assets = Buy(balance, df)
            date += datetime.timedelta(days=7)
        return balance_progress
