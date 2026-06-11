import pandas as pd

from backtest import Backtest

ticker = "HDFCBANK.NS"

holding_period = 7

strategies = [

    "hurst",

    "momentum",

    "mean_reversion"

]

results = []

for strat in strategies:

    bt = Backtest(

        ticker,

        holding_period=holding_period,

        mode=strat

    )

    bt.run()

    results.append({

        "Strategy": strat,

        "Return": bt.TotalReturn(),

        "Win Rate": bt.WinRate(),

        "Sharpe": bt.SharpeRatio(),

        "Drawdown": bt.max_drawdown()

    })

buyhold = Backtest(
    ticker
)

results.append({

    "Strategy": "buy_and_hold",

    "Return": buyhold.BuyAndHold(),

    "Win Rate": None,

    "Sharpe": None,

    "Drawdown": None

})

df = pd.DataFrame(results)

print(df)

df.to_csv(

    "strategy_comparison.csv",

    index=False

)