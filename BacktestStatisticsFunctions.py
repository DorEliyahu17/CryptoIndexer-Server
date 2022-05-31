def BacktestHODL(price_action: list[float], initial_balance: float=1000):
    balance_progress = [initial_balance]
    for i in range(1, len(price_action)):
        balance_progress.append(balance_progress[-1] * (price_action[i]/price_action[i - 1]))
    return balance_progress

def ROI(last_balance: float, initial_balance: float):
    return last_balance/initial_balance
 