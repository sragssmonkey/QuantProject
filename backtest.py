from pnl import ROI
from account import Account
import numpy as np
class Backtest:
    def __init__(self):
        pass 

    def SharpeRatio(self):
        ret=self.pnl.ROI.return_val()
        mean_return = np.mean(ret)
        vol=np.std(ret)
        sharpe=mean_return/vol
        return sharpe
    
    def WinRate(self):
        trades=np.array([])
        pnl_vals=self.pnl.ROI.pnl()
        win_trade=np.array([])
        trades.append(pnl_vals)
        for i in range(trades):
            if trades[i]>0:
                win_trade.append(trades[i])
            else:
                win_trade.append(0)
        win_rate=(np.count_nonzero(win_trade)/len(trades))*100
        return win_rate
    
    def max_drawdown(self):
        equity=self.account.balance()
        peak = equity[0]
        max_dd = 0

        for value in equity:

            peak = max(peak, value)

            drawdown = (peak - value) / peak

            max_dd = max(max_dd, drawdown)

        return max_dd * 100


