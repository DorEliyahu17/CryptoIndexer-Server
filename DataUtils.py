import pandas as pd
import json
import random
from os import path
from datetime import date, datetime, timedelta
from binance import Client

current_path = path.realpath(path.dirname(__file__))

with open(f'{current_path}/KEYS.json') as f:
    key_dict = json.load(f)
    apiKey = key_dict['binance_key']
    secret = key_dict['binance_secret']
    client = Client(apiKey, secret)

earliest_top_market_date = date(2017, 3, 19)


def GetHistoricalPriceData(symbol: str) -> pd.DataFrame:
    try:
        saved_df = pd.read_csv(
            f'{current_path}/Data/Symbols/{symbol}.csv', index_col=0)
        last_date = saved_df.iloc[-1]['Close time']
        if datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S.%f') > datetime.now() - timedelta(days=7):
            return saved_df

        ret = pd.concat(
            [saved_df, __DownloadBinanceHistoricalData(symbol, last_date)])
        ret.to_csv(f'{current_path}/Data/Symbols/{symbol}.csv')
        return ret
    except:
        ret = __DownloadBinanceHistoricalData(symbol)
        ret.to_csv(f'{current_path}/Data/Symbols/{symbol}.csv')
        return ret


def GetTopMarketData(date: date) -> pd.DataFrame:
    if date < earliest_top_market_date:
        raise Exception(
            f'date given is less than the earliest data date ({earliest_top_market_date}) available.')
    try:
        return pd.read_csv(f'{current_path}/Data/TopMCWeekly/{date}.csv')
    except:
        return None


def __DownloadBinanceHistoricalData(symbol: str, from_date: date | pd.Timestamp = None):
    from_date = str(from_date) if from_date is not None else '1 Jan, 2012'
    historical = client.get_historical_klines(symbol + 'USDT', '1w', from_date)
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades',
                       'TB Base Volume', 'TB Quote Volume', 'Ignore']
    hist_df['Open time'] = pd.to_datetime(hist_df['Open time'], unit='ms')
    hist_df['Close time'] = pd.to_datetime(hist_df['Close time'], unit='ms')
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume',
                       'Quote asset volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(
        pd.to_numeric, axis=1)
    data = hist_df.iloc[:-1, 1:7]
    return data


def GetAllSymbolsInfo() -> list[dict[str, str]]:
    all_usdt_tickers = [x['symbol'][:-4]
                        for x in client.get_all_tickers() if x['symbol'].endswith('USDT')]
    all_symbols = client.get_all_coins_info()

    all_symbols_dict = {}
    for symbol in all_symbols:
        all_symbols_dict[symbol['coin']] = symbol

    to_ret = []
    for symbol in all_usdt_tickers:
        if symbol in all_symbols_dict and all_symbols_dict[symbol]['trading']:
            d = {}
            d['symbol'] = symbol
            d['name'] = all_symbols_dict[symbol]['name']
            d['red'] = random.randint(0, 255)
            d['green'] = random.randint(0, 255)
            d['blue'] = random.randint(0, 255)
            to_ret.append(d)

    return to_ret
