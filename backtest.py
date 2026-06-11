import yfinance as yf
import numpy as np
import pandas as pd
from account import Account
from pnl import ROI
import os

from timeseries import (TimeSeries,HurstExponent,Decision)
class Backtest:
    def __init__(self,ticker,period="1y",initial_balance=100000,holding_period=5,mode="hurst"):
        self.ticker =ticker
        data = yf.download(ticker,period=period)
        self.prices = (data["Close"].values.flatten().tolist())
        self.account = Account(initial_balance)
        self.trade_log = []
        self.equity_curve = [initial_balance]
        self.roi = ROI(self.prices)
        self.holding_period = holding_period
        self.mode=mode
    
    def run(self):
        lookback = 100
        day = lookback

        while day < len(self.prices) - self.holding_period:

            window = self.prices[day-lookback:day]
            ts = TimeSeries([],window)
            returns = ts.time_series()
            hurst = HurstExponent(returns).hurst()
            decision = Decision(hurst,"STOCK",window)
            if self.mode == "hurst":

                decision = Decision(
                    hurst,
                    "STOCK",
                    window
                )

                strategy = decision.get_strategy()

            elif self.mode == "momentum":

                from momentumtrading import Momentum

                strategy = Momentum(
                    window
                )

            elif self.mode == "mean_reversion":

                from meanreversion import MeanReversion

                strategy = MeanReversion(
                    "STOCK",
                    window
                )

            else:

                strategy = None

            if strategy is None:

                day += 1

                continue
            signal = strategy.signal()
            if signal == "HOLD":
                day+=1
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
            exit_day = min(day + self.holding_period,len(self.prices)-1)
            
            exit_price = self.prices[exit_day]
            day = exit_day + 1

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
    def BuyAndHold(self):

        return (

            (self.prices[-1] - self.prices[0])
            /
            self.prices[0]

        ) * 100
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


    def export_summary(self, filename="all_results.csv"):

        summary = pd.DataFrame([{

            "Company Name": self.ticker,

            "Final Balance": self.FinalBalance(),

            "Total Return": self.TotalReturn(),

            "Win Rate": self.WinRate(),

            "Sharpe Ratio": self.SharpeRatio(),

            "Max Drawdown": self.max_drawdown()

        }])

        if os.path.exists(filename):

            summary.to_csv(
                filename,
                mode="a",
                header=False,
                index=False
            )

        else:

            summary.to_csv(
                filename,
                index=False
            )
    def export_trades(self):
        filename="trades.csv"
        df=pd.DataFrame(self.trade_log)
        df.to_csv(filename,index=False)
        print(f"Trade logs saved to {filename}")
