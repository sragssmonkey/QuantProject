from timeseries import TimeSeries

class Momentum:
    def __init__(self,prices):
        self.prices=prices
        ts = TimeSeries([], prices)
        self.returns_log = ts.time_series()
        self.mean_returns = None
        self.latest_price = None
        self.latest_ema = None
        self.RSI = None
        
    def momentumtrad(self):
        mean_returns = (
            sum(self.returns_log)
            / len(self.returns_log)
        )
        self.mean_returns = mean_returns
        if mean_returns>0:
            return "Trend is upwards"
        elif mean_returns<0:
            return "Trend is downwards"
        return "Neutral"
    
    def ExponentialMovingAverage(self, period=20):
        prices = self.prices
        alpha = 2 / (period + 1)
        ema_values = []
        sma = sum(prices[:period]) / period
        ema_values.append(sma)
        for price in prices[period:]:
            ema_today = (
                price * alpha
                +
                ema_values[-1] * (1 - alpha)
            )

            ema_values.append(ema_today)
        self.latest_price = prices[-1]

        self.latest_ema = ema_values[-1]

        if self.latest_price > self.latest_ema:
            return "BUY"

        else:
            return "SELL"
    
    def RelativeStrengthIndex(self, period=14):
        gains = []
        losses = []
        for i in range(1, len(self.prices)):
            diff = self.prices[i] - self.prices[i-1]
            if diff > 0:
                gains.append(diff)
                losses.append(0)
            elif diff < 0:
                gains.append(0)
                losses.append(abs(diff))
            else:
                gains.append(0)
                losses.append(0)
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        for i in range(period, len(gains)):
            avg_gain = (
                (avg_gain * (period - 1))
                + gains[i]
            ) / period

            avg_loss = (
                (avg_loss * (period - 1))
                + losses[i]
            ) / period
        if avg_loss == 0 and avg_gain == 0:
            RSI = 50
        elif avg_loss == 0:
            RSI = 100
        else:
            RS = avg_gain / avg_loss
            RSI = 100 - (100 / (1 + RS))
        self.RSI = RSI

        if RSI < 30:
            return "BUY"
        elif RSI > 70:
            return "SELL"
        else:
            return "HOLD"
        
    def finaldecision(self):
        if (
            self.mean_returns > 0
            and
            self.latest_price > self.latest_ema
            and
            self.RSI < 60
        ):
            return "BUY"
        else:
            return "SELL"
    
    def __str__(self):
        trend = self.momentumtrad()
        ema_signal = self.ExponentialMovingAverage()
        rsi_signal = self.RelativeStrengthIndex()
        return (
            f"Momentum Strategy\n"
            f"Trend: {trend}\n"
            f"EMA Signal: {ema_signal}\n"
            f"RSI Signal: {rsi_signal}"
        )

