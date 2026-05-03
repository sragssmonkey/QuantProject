import math
class MeanReversion:
    def __init__(self,company:str,prices:list)->None:
        self.company=company
        self.prices=prices
    
    def zscore(self):
        historic_mean=int(sum(self.prices)/len(self.prices))
        deviation = []
        for price in self.prices:
            deviation.append(price - historic_mean)        
        deviation_sq = []
        for d in deviation:
            deviation_sq.append(d * d)
        standard_deviation=math.sqrt(sum(deviation_sq)/len(self.prices)-1)
        current_deviation = deviation[-1]
        z_score=current_deviation/standard_deviation
        return z_score
    def book_trade(self):

        z=self.zscore()
        if z > 2:
            return"SHORT THIS STOCK(SELL)"
        elif z < -2:
            return"GO LONG(BUY)"
        else:
            return "HOLD"
    def __str__(self) -> str:
        z = self.zscore()
        return f'{self.company}: Z-score={z:.2f} → {self.book_trade()}'



