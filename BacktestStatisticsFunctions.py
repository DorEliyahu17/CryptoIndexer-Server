def BacktestHODL(price_action, initial_balance=1000):
    balance_progress = [initial_balance]
    for i in range(1, len(price_action)):
        balance_progress.append(balance_progress[-1] * (price_action[i]/price_action[i - 1]))
    return balance_progress

def ROI(last_balance, initial_balance):
    return last_balance/initial_balance

def BacktestCustomIndex(returns, initial_balance):
    balance_progress = [initial_balance]
    for i in range(1, len(returns)):
        balance_progress.append(balance_progress[-1] + balance_progress[-1]*returns[i])
    return balance_progress

def GenerateSymbolReturns(price_action):
    returns = []
    for i in range(1, len(price_action)):
        returns.append((price_action[i] - price_action[i - 1])/price_action[i - 1])
    return returns

def AvgReturn(price_action):
    returns = GenerateSymbolReturns(price_action)
    return sum(returns)/len(returns)

def StdReturn(price_action):
    avg_ret = AvgReturn(price_action)
    returns = GenerateSymbolReturns(price_action)
    std = 0
    for r in returns:
        std += (r -avg_ret)**2
    return std**0.5

def PearsonCorrelation(price_action_1, price_action_2):
    def E(l):
        return sum(l)/len(l)

    X = price_action_1
    Y = price_action_2
    X2 = [x**2 for x in X]
    Y2 = [y**2 for y in Y]
    XY = [x*y for x,y in zip(X, Y)]

    std_XY = E(XY) - E(X)*E(Y)
    std_X = (E(X2) - E(X)**2)**0.5
    std_Y = (E(Y2) - E(Y)**2)**0.5

    return std_XY/(std_X*std_Y)

def SharpeRatio(balance_progress):
    return AvgReturn(balance_progress)/StdReturn(balance_progress)

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
