from sys import argv
import json
from Index import Index

try:
    arg_ind: dict[str, float] = json.loads(argv[1])
    initial_balance = json.loads(argv[2])

    index = Index('tmp', 'tmp')

    for symbol, weight in arg_ind.items():
        index.AddSymbol(symbol.replace('"', ''), float(weight))

    backtest_res = index.Backtest(initial_balance, 0.001)

    dic_to_ret = {
        "success": True,
        "data":
            {
                "dates": [str(x) for x in backtest_res[0]],
                "balance_progress": backtest_res[1]
            }
    }
except Exception as e:
    dic_to_ret = {"success": False, "data": str(e)}

print(json.dumps(dic_to_ret))
