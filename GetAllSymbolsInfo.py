from DataFetcher import GetAllSymbolsInfo

try:
    dict_to_ret = {
        "success": True,
        "data": GetAllSymbolsInfo()
    }
except Exception as e:
    #dict_to_ret = {"success": False, "data": str(e)}
    raise e

with open('res.txt', 'w', encoding='utf8') as f:
    f.write(str(str(dict_to_ret).encode('utf8')))

print(dict_to_ret)
