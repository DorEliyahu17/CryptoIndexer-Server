from typing import Dict
from sys import argv
import json
from Index import Index

arg_ind: Dict[str, float] = json.loads(argv[1])

index = Index('tmp', 'tmp')

for symbol, weight in arg_ind.items():
    index.AddSymbol(symbol, weight)

backtest_res = index.Backtest(1000, 0.004)

dic_to_ret = {"success": True, "data": backtest_res}

print(json.dumps(dic_to_ret))
