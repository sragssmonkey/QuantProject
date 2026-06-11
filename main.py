from backtest import Backtest

for hold in range(1,31):

    bt = Backtest(
        "TCS.NS",
        holding_period=hold
    )

    bt.run()

    print(
        hold,
        bt.TotalReturn()
    )
