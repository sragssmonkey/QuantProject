from backtest import Backtest
bt = Backtest("RELIANCE.NS")

bt.run()

print("Final Balance:", bt.FinalBalance())
print("Total Return:", bt.TotalReturn())
print("Win Rate:", bt.WinRate())
print("Sharpe Ratio:", bt.SharpeRatio())
print("Max Drawdown:", bt.max_drawdown())

bt.plot_equity_curve()