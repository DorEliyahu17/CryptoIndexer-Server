import pandas as pd
import datetime
import matplotlib.pyplot as plt

def Buy(df: pd.DataFrame, balance: float) -> dict:
    total_market_cap = df['Market Cap'].head(10).sum()
    df['Percent'] = df['Market Cap']/total_market_cap
    
    bag = {}
    balance -= balance*0.001
    for i in range(10):
        if not df['Symbol'][i] == 'STO': 
            bag[df['Symbol'][i]] = balance*df['Percent'][i]/df['Price'][i]
        else:
            bag['BTC'] += balance*df['Percent'][i]/df['Price'][0]
    return bag

def Sell(df: pd.DataFrame, bag: dict) -> float:
    balance = 0
    for symbol in bag.keys():
            balance += bag[symbol]*df[df['Symbol'] == symbol]['Price'].iloc[0]
    balance -= balance*0.001
    return balance

date = datetime.date(2017, 3, 19)
df = pd.read_csv('Data/' + str(date) + '.csv')
balance_progress = [1000]
bag = Buy(df, 1000)
date += datetime.timedelta(days=7)
while date < datetime.date.today():
    df = pd.read_csv('Data/' + str(date) + '.csv')
    balance = Sell(df, bag)
    balance_progress.append(balance)
    bag = Buy(df, balance)
    date += datetime.timedelta(days=7)

print(balance)
fig = plt.figure(figsize=(20,8))
plt.plot(balance_progress)