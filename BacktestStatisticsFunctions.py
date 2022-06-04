def BacktestHODL(price_action: list[float], initial_balance: float=1000):
    balance_progress = [initial_balance]
    for i in range(1, len(price_action)):
        balance_progress.append(balance_progress[-1] * (price_action[i]/price_action[i - 1]))
    return balance_progress

def ROI(last_balance: float, initial_balance: float):
    return last_balance/initial_balance

def MaxDrawdown(balance_progress):
    max_drawdown = 0
    peak = balance_progress[0]
    i = 1
    while i < len(balance_progress):
        valley = balance_progress[i]
        while i < len(balance_progress) and balance_progress[i] < peak:
            if balance_progress[i] < valley:
                valley = balance_progress[i]
            i += 1
        max_drawdown = min(max_drawdown, (valley - peak)/peak)
        if i < len(balance_progress):
            peak = balance_progress[i]
        i += 1
    return max_drawdown