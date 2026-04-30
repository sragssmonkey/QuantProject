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



Infosys=MeanReversion("Infosys",[272.19, 273.67, 270.97, 272.36, 273.81, 
     273.40, 273.76, 273.08, 271.86, 271.01, 
     267.26, 262.36, 260.33, 259.04, 259.37, 
     260.25, 261.65])

print(Infosys)

TCS = MeanReversion("TCS",[
    3495.25, 3502.10, 3489.80, 3498.45, 3510.60,
    3505.20, 3512.75, 3508.90, 3499.55, 3492.30,
    3475.40, 3462.15, 3458.20, 3449.75, 3455.60,
    3468.35, 3472.90
])
print(TCS)

Tesla= MeanReversion("Tesla",[
    520.15, 528.40, 515.75, 530.60, 540.25,
    535.10, 548.90, 560.35, 552.20, 540.75,
    525.60, 510.25, 498.80, 505.40, 515.90,
    525.30, 538.75
])
print(Tesla)

Test_prices = [
    100, 101, 102, 100, 99,
    98, 97, 96, 95, 94,
    93, 92, 91, 90, 89,
    88, 70   # big drop → should trigger BUY
]

TestStock = MeanReversion("Test", Test_prices)

print(TestStock)

print(Infosys.zscore())