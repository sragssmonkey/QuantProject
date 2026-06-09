import yfinance as yf
import numpy as np

from account import Account
from pnl import ROI

from timeseries import (TimeSeries,HurstExponent,Decision)
class Backtest:
    def __init__(self,ticker,period="1y",initial_balance=100000):
        data = yf.download(ticker,period=period)
        self.prices = (data["Close"].values.flatten().tolist())
        self.account = Account(initial_balance)
        self.trade_log = []
        self.equity_curve = [initial_balance]
        self.roi = ROI(self.prices)
    
    def run(self):
        lookback = 100
        for day in range(lookback,len(self.prices) - 5):
            window = self.prices[day-lookback:day]
            ts = TimeSeries([],window)
            returns = ts.time_series()
            hurst = HurstExponent(returns).hurst()
            decision = Decision(hurst,"STOCK",window)
            strategy = (decision.get_strategy())
            if strategy is None:
                continue
            signal = strategy.signal()
            if signal == "HOLD":
                continue
            entry_price = (self.prices[day])
            roi = ROI(window)
            stop_distance = (roi.stop_loss(entry_price))
            if signal == "LONG":
                stop_price = (entry_price-stop_distance)
            elif signal == "SHORT":
                stop_price = (entry_price+stop_distance)
            else:
                continue
            quantity = (roi.position_size(self.account.balance,entry_price,stop_price))

            exit_price = (self.prices[day + 5])

            pnl = (self.roi.calculate_pnl(signal,entry_price,exit_price,quantity))
            print("Entry:", entry_price)

            print("Stop Distance:", stop_distance)

            print("Stop Price:", stop_price)
            print("Quantity:", quantity)
            print("PnL:", pnl)
            self.account.update_balance(pnl)
            self.equity_curve.append(self.account.balance)
            self.trade_log.append({

                "hurst": hurst,

                "signal": signal,

                "entry": entry_price,

                "exit": exit_price,

                "qty": quantity,

                "pnl": pnl

            })

        return self.trade_log

    def SharpeRatio(self):
        pnls = [trade["pnl"] for trade in self.trade_log]
        if len(pnls) < 2:
            return 0
        std = np.std(pnls)
        if std == 0:
            return 0
        return np.mean(pnls) / std
    
    def WinRate(self):
        if len(self.trade_log) == 0:
            return 0
        wins = sum(1 for trade in self.trade_log if trade["pnl"] > 0)

        return (wins/len(self.trade_log)) * 100
    
    def max_drawdown(self):

        equity = self.equity_curve
        if len(equity) == 0:
            return 0
        peak = equity[0]
        max_dd = 0
        for value in equity:
            peak = max(peak,value)
            drawdown = (peak - value) / peak
            max_dd = max(max_dd,drawdown)
        return max_dd * 100

    def TotalReturn(self):

        initial = self.equity_curve[0]
        final = self.equity_curve[-1]
        return ((final - initial)/initial) * 100

    def FinalBalance(self):
        return self.account.balance
    
    def plot_equity_curve(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,5))
        plt.plot(self.equity_curve)
        plt.title("Equity Curve")
        plt.xlabel("Trade Number")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.show()
