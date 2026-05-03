import yfinance as yf

from timeseries import TimeSeries, HurstExponent,Decision
from meanreversion import MeanReversion
from momentumtrading import Momentum



data = yf.download("RELIANCE.NS", period="1y")

prices = data["Close"].values.flatten().tolist()

ts = TimeSeries([], prices)

returns = ts.time_series()

hurst_calc = HurstExponent(returns)

H = hurst_calc.hurst()

print("H:", H)
decision = Decision(
    
    H,
    "REL",
    prices
)
print(decision)
strategy = decision.get_strategy()

if strategy:
    print(strategy)
