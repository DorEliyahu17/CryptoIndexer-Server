from sys import argv
from DataFetcher import GetHistoricalPriceData

try:
    symbols_prices = {}
    for i in range(1, len(argv)):
        try:
            hist_df = GetHistoricalPriceData(argv[i])
        except:
            pass
        else:
            symbols_prices[argv[i]] = {"dates": list(hist_df['Close time']), "prices": list(hist_df['Close'])}

    dict_to_ret = {
        "success": True,
        "data": symbols_prices
    }
except Exception as e:
    dict_to_ret = {
        "success": False,
        "data": str(e)
}

print(dict_to_ret)
