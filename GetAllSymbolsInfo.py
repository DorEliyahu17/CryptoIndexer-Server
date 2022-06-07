from DataUtils import GetAllSymbolsInfo
import sys
import json

try:
    dict_to_ret = {
        "success": True,
        "data": GetAllSymbolsInfo()
    }
except Exception as e:
    dict_to_ret = {"success": False, "data": str(e)}

sys.stdout.buffer.write(json.dumps(dict_to_ret).encode('utf8'))
