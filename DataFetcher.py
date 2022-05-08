import pandas as pd
import requests
import json
from os import path
from datetime import date, datetime
from binance import Client

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

    df.to_csv(f'Data/{datetime.now().date()}.csv')

earliest_top_market_date = date(2017, 3, 19)

def GetHistoricalPriceData(symbol):
    with open(path.join(path.realpath(path.dirname(__file__)), 'KEYS.json')) as f:
        key_dict = json.load(f)
    apiKey = key_dict['binance_key']
    secret = key_dict['binance_secret']
    client = Client(apiKey, secret)
    historical = client.get_historical_klines(symbol, '1w', '1 Jan, 2012')
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades',
                       'TB Base Volume', 'TB Quote Volume', 'Ignore']
    hist_df['Open time'] = pd.to_datetime(hist_df['Open time']/1000, unit='s')
    hist_df['Close time'] = pd.to_datetime(
        hist_df['Close time']/1000, unit='s')
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume',
                       'Quote asset volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(
        pd.to_numeric, axis=1)
    data = hist_df.iloc[:-1, 1:7]
    return data

def GetTopMarketData(date: date) -> pd.DataFrame:
    if date < earliest_top_market_date:
        raise Exception(f'date given is less than the earliest data date ({earliest_top_market_date}) available.')
    try:
        return pd.read_csv(f'Data/{date}.csv')
    except:
        return None
