from backtest import Backtest
bt = Backtest("NESTLEIND.NS")

bt.run()

print("Final Balance:", bt.FinalBalance())
print("Total Return:", bt.TotalReturn())
print("Win Rate:", bt.WinRate())
print("Sharpe Ratio:", bt.SharpeRatio())
print("Max Drawdown:", bt.max_drawdown())

bt.plot_equity_curve()
bt.export_trades()
bt.export_summary()