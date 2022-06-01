from DataFetcher import GetAllSymbolsInfo

try:
    dict_to_ret = {
        "success": True,
        "data": GetAllSymbolsInfo()
    }
except Exception as e:
    dict_to_ret = {"success": False, "data": str(e)}

print(dict_to_ret)
