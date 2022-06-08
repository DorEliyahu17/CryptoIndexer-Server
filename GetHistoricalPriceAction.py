import sys
import json
from DataUtils import GetHistoricalPriceData


try:
    symbols_prices = {}
    for i in range(1, len(sys.argv)):
        try:
            hist_df = GetHistoricalPriceData(sys.argv[i])
        except:
            pass
        else:
            symbols_prices[sys.argv[i]] = {
                "dates": [s.split(' ')[0] for s in hist_df['Close time']], 
                "prices": list(hist_df['Close'])
            }

    dict_to_ret = {
        "success": True,
        "data": symbols_prices
    }
except Exception as e:
    dict_to_ret = {
        "success": False,
        "data": str(e)
}

print(json.dumps(dict_to_ret).encode('utf8'))
