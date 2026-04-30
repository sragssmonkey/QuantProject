import yfinance as yf
from meanreversion import MeanReversion


data = yf.download("INFY.NS", period="3mo")
print(data)

prices = data["Close"].values.flatten().tolist()

Infosys = MeanReversion("Infosys", prices)

print(Infosys)
