from DataFetcher import GetAllSymbolsInfo
import sys
import json

try:
    dict_to_ret = {
        "success": True,
        "data": GetAllSymbolsInfo()
    }
except Exception as e:
    dict_to_ret = {"success": False, "data": str(e)}

to_ret = json.dumps(dict_to_ret)
to_ret = to_ret.encode('utf8')

sys.stdout.buffer.write(to_ret)
