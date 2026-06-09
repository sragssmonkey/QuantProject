from pnl import ROI

class Account:
    def __init__(self,acc_balance,entry_price,exit_price):
        self.acc_balance=acc_balance
        self.entry_price=entry_price
        self.exit_price=self.exit_price
        return acc_balance,entry_price,exit_price
    
    
    def balance(self):
        balance_sheet=[]
        pnl_update=self.ROI.pnl()
        self.acc_balance+=pnl_update
        balance_sheet.append(self.acc_balance)
        return balance_sheet
    