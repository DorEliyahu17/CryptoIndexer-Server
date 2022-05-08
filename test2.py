from sys import argv
import json
from os import path
from time import sleep
# print("argv[1]=" + argv[1])

#x = json.loads(argv[1])

sleep(5)

print(path.abspath(path.dirname(__file__)))
with open(path.join(path.realpath(path.dirname(__file__)), 'KEYS.json')) as f:
    keys_dict = json.load(f)
print(keys_dict)

# print(x)
# print(x['BTC'])
# print(x['ETH'])
# print(x['SOL'])
# print(type(x))
# print(type(x['BTC']))

#res = [1.1, 2.5, 3.4, 8]

#dic_to_ret = {"success": True, "data": res}


#print(json.dumps(x))
