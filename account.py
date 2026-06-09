class Account:
    def __init__(self, initial_balance=100000):
        self.balance = initial_balance
        self.entry_price = None
        self.exit_price = None
        self.position_size = 0

    def update_balance(self, pnl):
        self.balance += pnl

    def get_balance(self):
        return self.balance
    
    
    