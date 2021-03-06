import sys
import json
from DataUtils import GetHistoricalPriceData
from Index import Index

try:
    indexes_json = json.loads(sys.argv[1])
    indexes = []
    for i in indexes_json:
        index = Index()
        for d in i:
            index.AddSymbol(d['symbol'], d['weight'])
        indexes.append(index)

    gains = []
    for i in indexes:
        r = 0
        for symbol, weight in i.symbols_weights.items():
            prices = GetHistoricalPriceData(symbol)['Close']
            r += weight*(prices.iloc[-1] - prices.iloc[-2])/prices.iloc[-2]
        gains.append(r)

    dic_to_ret = {'success': True, 'data': gains}
except Exception as e:
    dic_to_ret = {'success': False, 'data': str(e)}

sys.stdout.buffer.write(json.dumps(dic_to_ret).encode('utf8'))