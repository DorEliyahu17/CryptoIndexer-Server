from sys import argv
import json
from Index import Index
from DataFetcher import GetHistoricalPriceData
import BacktestStatisticsFunctions as bsf

def GenerateSymbolRes(symbol: str, initial_balance: float) -> dict:
    res = {}
    res["symbol"] = symbol
    price_action = GetHistoricalPriceData(symbol)
    res["dates"] = [str(x) for x in price_action["Close time"]]
    res["balance_progress"] = bsf.BacktestHODL(price_action["Close"], initial_balance)
    res["roi"] = bsf.ROI(res["balance_progress"][-1], initial_balance)
    return res

print(argv[1])
try:
    arg_ind: dict[str, float] = json.loads(argv[1])
    try:
        initial_balance = int(argv[2])
    except:
        initial_balance = 1000

    index = Index('tmp', 'tmp')

    for symbol, weight in arg_ind.items():
        print(symbol)
        index.AddSymbol(symbol.replace('"', ''), float(weight))

    backtest_res = index.Backtest(initial_balance, 0.001)
    symbols_res = [GenerateSymbolRes(x, initial_balance) for x in index.symbols_weights.keys()]

    dic_to_ret = {
        "success": True,
        "data":
            {
                "index": {
                    "dates": [str(x) for x in backtest_res[0]],
                    "balance_progress": backtest_res[1],
                    "roi": bsf.ROI(backtest_res[1][-1], initial_balance)
                },
                "symbols": symbols_res
            }
    }

except Exception as e:
    dic_to_ret = {"success": False, "data": str(e)}



print(json.dumps(dic_to_ret))
