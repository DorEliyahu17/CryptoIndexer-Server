import pandas as pd
import requests
import json
from os import path
from datetime import date, datetime, timedelta
from binance import Client
import binance.exceptions

current_path = path.realpath(path.dirname(__file__))

if __name__ == '__main__':
    API_KEY = 'bc156928-6ada-4045-87f7-c69b79499b32'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {'X-CMC_PRO_API_KEY':API_KEY}

    response = requests.get(url, headers=headers)

    data = json.loads(response.content)

    ranks = [x['cmc_rank'] for x in data['data']]
    names = [x['name'] for x in data['data']]
    symbols = [x['symbol'] for x in data['data']]
    market_caps = [x['circulating_supply']*x['quote']['USD']['price'] for x in data['data']]
    prices = [x['quote']['USD']['price'] for x in data['data']]

    df = pd.DataFrame({
        'Rank': ranks, 
        'Name': names, 
        'Symbol': symbols, 
        'Market Cap': market_caps, 
        'Price': prices, 
        'Date': datetime.now().date()
        })

    df.to_csv(f'{current_path}/Data/TopMC/{datetime.now().date()}.csv')

earliest_top_market_date = date(2017, 3, 19)

def GetHistoricalPriceData(symbol: str) -> pd.DataFrame:
    try:
        saved_df = pd.read_csv(f'{current_path}/Data/Symbols/{symbol}.csv')
        last_date = list(saved_df['Close time'])[-1]
        if last_date > datetime.now() - timedelta(days=7):
            return saved_df
        ret = pd.concat([saved_df, __DownloadBinanceHistoricalData(symbol, last_date)])
        ret.to_csv(f'{current_path}/Data/Symbols/{symbol}.csv')
        return ret
    except:
        ret = __DownloadBinanceHistoricalData(symbol)
        ret.to_csv(f'{current_path}/Data/Symbols/{symbol}.csv')
        return ret
    

def GetTopMarketData(date: date) -> pd.DataFrame:
    if date < earliest_top_market_date:
        raise Exception(f'date given is less than the earliest data date ({earliest_top_market_date}) available.')
    try:
        return pd.read_csv(f'{current_path}/Data/TopMC/{date}.csv')
    except:
        return None

#Add Binance API Exception catching for incorrect symbol

def __DownloadBinanceHistoricalData(symbol: str, from_date: date | pd.Timestamp=None):
    with open(f'{current_path}/KEYS.json') as f:
        key_dict = json.load(f)
    apiKey = key_dict['binance_key']
    secret = key_dict['binance_secret']
    client = Client(apiKey, secret)
    from_date = str(from_date) if from_date is not None else '1 Jan, 2012'
    historical = client.get_historical_klines(symbol + 'USDT', '1w', from_date)
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades',
                       'TB Base Volume', 'TB Quote Volume', 'Ignore']
    hist_df['Open time'] = pd.to_datetime(hist_df['Open time']/1000, unit='s')
    hist_df['Close time'] = pd.to_datetime(hist_df['Close time']/1000, unit='s')
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume',
                       'Quote asset volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(
        pd.to_numeric, axis=1)
    data = hist_df.iloc[:-1, 1:7]
    return data
