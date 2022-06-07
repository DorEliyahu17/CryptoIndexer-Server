import pandas as pd
import requests
import json
from os import path
from datetime import datetime


if __name__ == '__main__':
    api_key = 'bc156928-6ada-4045-87f7-c69b79499b32'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    current_path = path.realpath(path.dirname(__file__))

    headers = {'X-CMC_PRO_API_KEY': api_key}

    response = requests.get(url, headers=headers)

    data = json.loads(response.content)

    ranks = [x['cmc_rank'] for x in data['data']]
    names = [x['name'] for x in data['data']]
    symbols = [x['symbol'] for x in data['data']]
    market_caps = [x['circulating_supply']*x['quote']
                   ['USD']['price'] for x in data['data']]
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
