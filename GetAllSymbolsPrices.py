import DataUtils
import pandas as pd
import json
import sys

try:
    df = pd.DataFrame(columns=['Symbol', 'Name', 'Price', 'Weekly High', 'Weekly Low', 'Weekly % Change'])
    all_symbols = DataUtils.GetAllSymbolsInfo()
    df['Symbol'] = [x['symbol'] for x in all_symbols]
    df['Name'] = [x['name'] for x in all_symbols]
    df.set_index('Symbol', drop=False, inplace=True)

    for symbol in df.index:
        price_action = DataUtils.GetHistoricalPriceData(symbol)
        if len(price_action) > 0:
            df['Price'][symbol] = price_action.iloc[-1]['Close']
            df['Weekly High'][symbol] = price_action.iloc[-1]['High']
            df['Weekly Low'][symbol] = price_action.iloc[-1]['Low']
            df['Weekly % Change'][symbol] = (price_action.iloc[-1]['Close'] - price_action.iloc[-1]['Open'])/price_action.iloc[-1]['Open']

    dict_to_ret = {'success': True, 'data': df.to_dict('records')}

except Exception as e:
    dict_to_ret = {'success': False, 'data': str(e)}

sys.stdout.buffer.write(json.dumps(dict_to_ret).encode('utf8'))