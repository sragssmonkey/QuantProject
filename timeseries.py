import math
import numpy as np

class TimeSeries:
    def __init__(self,time_stamp:list,prices:list)->None:
        self.time_stamp=time_stamp
        self.prices=prices
    
    def time_series(self):
        returns_log=[]
        for i in range(1,len(self.prices)):
            rt=math.log(self.prices[i]/self.prices[i-1])
            returns_log.append(rt)
        return returns_log
    
class HurstExponent:
    def __init__(self,returns_log)->None:
        self.returns_log=returns_log
        
    def splitperiods(self):
        n = len(self.returns_log)
        periods = []
        p = 8
        while p <= n // 2:
            periods.append(p)
            p *= 2
        return periods
    
    def hurst(self):

        periods = self.splitperiods()
        RS_values = []
        for p in periods:
            chunks = []
            for i in range(0, len(self.returns_log), p):
                chunk = self.returns_log[i:i+p]
                if len(chunk) == p:
                    chunks.append(chunk)

            RS_chunk_values = []
            for chunk in chunks:
                mean_val = np.mean(chunk)
                deviations = chunk - mean_val
                cumulative_dev = np.cumsum(deviations)
                R = max(cumulative_dev) - min(cumulative_dev)
                S = np.std(chunk)
                if S != 0:
                    RS = R / S
                    RS_chunk_values.append(RS)

            if len(RS_chunk_values) > 0:
                RS_values.append(np.mean(RS_chunk_values))
        log_RS = np.log(RS_values)
        log_periods = np.log(periods)
        H = np.polyfit(log_periods, log_RS, 1)[0]

        return H

class Decision:
    def __init__(self,H,company,prices)->None:
        
        self.company = company
        self.H = float(H)
        self.prices = prices
    def tradestrat(self):
        if self.H>0.55:
            return "TRENDING"
        elif self.H<0.45:
            return "REVERSING"
        else:
            return "NO EDGE"
    
    def get_strategy(self):

        if self.H < 0.45:
            from meanreversion import MeanReversion

            return MeanReversion(
                self.company,
                self.prices
            )
        elif self.H > 0.55:
            from momentumtrading import Momentum
            return Momentum(self.prices)

        return None
    def __str__(self) -> str:
        return f'H={self.H:.2f} → {self.tradestrat()}'

