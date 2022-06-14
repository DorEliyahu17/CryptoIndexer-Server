import sys
import json
import BacktestStatisticsFunctions as bsf
from TopCryptoIndex import TopCryptoIndex

try:
    initial_balance = int(sys.argv[1])

    top_index = TopCryptoIndex(10)
    backtest_res = top_index.Backtest(initial_balance, 0.001)

    dic_to_ret = {
        'success': True,
        'data': {
            'dates': [str(x) for x in backtest_res[0]],
            'balance_progress': backtest_res[1],
            'roi': bsf.ROI(backtest_res[1][-1], initial_balance),
            'max_drawdown': bsf.MaxDrawdown(backtest_res[1]),
            'sharpe_ratio': bsf.SharpeRatio(backtest_res[1]),
            'weekly_return_avg': bsf.AvgReturn(backtest_res[1]),
            'weekly_return_std': bsf.StdReturn(backtest_res[1]),
            'current_components': backtest_res[2].head(10).to_dict('records'),
        }
    }

except Exception as e:
    dic_to_ret = {'success': False, 'data': str(e)}

sys.stdout.buffer.write(json.dumps(dic_to_ret).encode('utf8'))