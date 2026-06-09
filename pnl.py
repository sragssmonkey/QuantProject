
import matplotlib.pyplot as plt
import numpy as np

class ROI:
    def __init__(self,prices):
        self.prices=prices
        self.trade_pnls = []
    
    def return_val(self):
        returns = []
        for i in range(1, len(self.prices)):
            r = (
                (self.prices[i] - self.prices[i - 1])
                /
                self.prices[i - 1]
            )
            returns.append(r)
        return returns

    def stop_loss(self):
        returns = self.return_val()
        volatility = np.std(returns)
        stop_distance = 2 * volatility
        return stop_distance

    
    def position_size(self,balance,entry_price,stop_price):
        account_risk = 0.02 * balance
        trade_risk = abs(entry_price - stop_price)
        if trade_risk == 0:
            return 0
        qty = int(account_risk / trade_risk)
        return qty
    
    def calculate_pnl(self,side,entry,exit_price,qty):
        if side == "LONG":
            pnl = (exit_price - entry) * qty
        elif side == "SHORT":
            pnl = (entry - exit_price) * qty
        else:
            pnl = 0
        self.trade_pnls.append(pnl)
        return pnl
    
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
        
    

        
    

