import sys
import json
from Index import Index
from DataUtils import GetHistoricalPriceData
import BacktestStatisticsFunctions as bsf

def GenerateSymbolRes(symbol, initial_balance, tail):
    res = {}
    res['symbol'] = symbol
    price_action = GetHistoricalPriceData(symbol).tail(tail).reset_index()

    res['dates'] = [s.split(' ')[0] for s in price_action['Close time']]
    res['balance_progress'] = bsf.BacktestHODL(
        price_action['Close'], initial_balance)
    res['roi'] = bsf.ROI(res['balance_progress'][-1], initial_balance)
    res['max_drawdown'] = bsf.MaxDrawdown(res['balance_progress'])
    res['sharpe_ratio'] = bsf.SharpeRatio(res['balance_progress'])
    res['weekly_return_avg'] = bsf.AvgReturn(res['balance_progress'])
    res['weekly_return_std'] = bsf.StdReturn(res['balance_progress'])
    return res


try:
    index_json = json.loads(sys.argv[1])

    try:
        initial_balance = int(sys.argv[2])
    except:
        initial_balance = 1000

    index = Index()
    for d in index_json:
        index.AddSymbol(d['symbol'], d['weight'])
    backtest_res = index.Backtest(initial_balance, 0.001)

    symbols_res = [GenerateSymbolRes(x, initial_balance, len(
        backtest_res[0])) for x in index.symbols_weights.keys()]

    correlations = {}
    for s1 in index.symbols_weights.keys():
        correlations[s1] = {}
        data1 = GetHistoricalPriceData(s1).tail(
            len(backtest_res[0])).reset_index()['Close']
        for s2 in index.symbols_weights.keys():
            if s1 != s2:
                data2 = GetHistoricalPriceData(s2).tail(
                    len(backtest_res[0])).reset_index()['Close']
                correlations[s1][s2] = bsf.PearsonCorrelation(data1, data2)

    dic_to_ret = {
        'success': True,
        'data':
            {
                'index': {
                    'dates': [s.split(' ')[0] for s in backtest_res[0]],
                    'balance_progress': backtest_res[1],
                    'roi': bsf.ROI(backtest_res[1][-1], initial_balance),
                    'max_drawdown': bsf.MaxDrawdown(backtest_res[1]),
                    'sharpe_ratio': bsf.SharpeRatio(backtest_res[1]),
                    'weekly_return_avg': bsf.AvgReturn(backtest_res[1]),
                    'weekly_return_std': bsf.StdReturn(backtest_res[1]),
                },
                'symbols': symbols_res,
                'correlations_matrix': correlations
            }
    }

except Exception as e:
    dic_to_ret = {"success": False, "data": str(e)}

sys.stdout.buffer.write(json.dumps(dic_to_ret).encode('utf8'))
