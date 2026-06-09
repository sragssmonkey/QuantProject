import math
from account import Account
from meanreversion import MeanReversion
import matplotlib.pyplot as plt
import numpy as np
from timeseries import TimeSeries
class ROI:
    def __init__(self,prices):
        self.prices=prices
        ts = TimeSeries([], prices)
        self.returns_log = ts.time_series()
    
    def return_val(self):
        returns_Daily=[]
        for i in self.returns_log:
            returns_Daily=[(self.returns_log[i]-self.returns_log[i-1])/self.returns_log[i-1]]*100
        return returns_Daily

    def StopLoss(self):
        ret=self.return_val()
        r=[]
        for i in ret:
            r= ret[i]**2

        volatility = np.std(r)
        stop_loss_order=volatility*2
        return stop_loss_order
    
    def PositionSizing(self):
        balance=self.Account.acc_balance()
        acc_risk=0.02*balance
        entry=self.Account.entry_price()
        trade_risk=entry-self.StopLoss()
        if trade_risk == 0:
            return 0
        position_size=acc_risk//trade_risk
        return position_size
    
    def pnl(self):

        entry = self.Account.entry_price()
        exit_price = self.Account.exit_price()

        qty = self.PositionSizing()

        side = self.MeanReversion.book_trade()

        if side == "LONG":
            pnl_ = qty * (exit_price - entry)

        elif side == "SHORT":
            pnl_ = qty * (entry - exit_price)

        self.trade_pnls.append(pnl_)

        return pnl_
    
    def plot_pnl(self):

        cumulative = np.cumsum(self.trade_pnls)
        start = np.concatenate(([0], cumulative[:-1]))
        plt.figure(figsize=(8,5))
        for i in range(len(self.trade_pnls)):
            plt.bar(
                i,
                self.trade_pnls[i],
                bottom=start[i],
                color='green' if self.trade_pnls[i] > 0 else 'red'
            )

        plt.axhline(0, color='black')
        plt.title("Waterfall Chart of Trade PnL")
        plt.xlabel("Trade Number")
        plt.ylabel("Cumulative PnL")

        plt.show()
        
    

        
    

