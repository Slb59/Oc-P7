"""
Optimize_v1 + class wallet
"""

import csv
from dataclasses import dataclass
from time import time

@dataclass
class Stock:
    """ a stock has a name, a price, a profit and a benefit=price*profit/100 """
    
    name: str
    price: float
    profit: float

    @property
    def benefit(self) -> float:
        return self.price * self.profit / 100

class Wallet:
    """ a wallet is a list of Stock
    all wallets have a max_invest """

    max_invest = 500

    def __init__(self, csv_file = None) -> None:
        """ a wallet can be init with a csv file
        the csv file need the columns name, price and profit """
        self.stocks = []
        self.csv_file = csv_file

        if self.csv_file is not None:
            self.load_dataset()

    def __repr__(self) -> str:
        result = ''
        result += (f'Actions du portefeuille: {len(self.stocks)}' + '\n')
        for stock in self.stocks:
            result +=(f"{stock.name} prix: {stock.price} € benefice: {stock.benefit} €" + '\n')
        result +=("Valeur du portefeuille:" + '\n')
        result +=(f'Coût total: {self.totalcost:.2f} €' + '\n')
        result +=(f'Benefice sur 2 ans: {self.totalbenef:.2f} €' + '\n')
        return result

    def __len__(self):
        return len(self.stocks)

    @property
    def totalcost(self) -> float:
        """ the totalcost is the sum of the price of the stocks in the wallet """
        return sum(stock.price for stock in self.stocks)
    
    @property
    def totalbenef(self) -> float:
        """ the totalbenef is the sum of the benef of the stocks in the wallet """
        return sum(stock.benefit for stock in self.stocks)
    
    def load_dataset(self):
        self.stocks = []
        with open(self.csv_file) as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                action = Stock(row["name"], float(row["price"]), float(row["profit"]))
                self.stocks.append(action)
        return self.stocks

def optimized(wallet: Wallet) -> Wallet:    
    best_wallet = Wallet()
    n = len(wallet)
    max_invest = int(wallet.max_invest*100)

    sol = [[0 for _ in range(max_invest+1)] for _ in range(n+1)]
    
    # first line : 0 stock is tested
    # last line : the nieme stock is tested
    for i_stock in range(n+1): 
        price_stock = int(wallet.stocks[i_stock-1].price*100) # line i_stock is the stock i_stock-1
        for cost in range(price_stock, max_invest+1):
            if i_stock ==0 or cost ==0:
                sol[i_stock][cost] = 0
            elif price_stock <= cost:
                sol[i_stock][cost] = max(
                    int(wallet.stocks[i_stock-1].benefit*100) + sol[i_stock-1][cost-price_stock],
                    sol[i_stock-1][cost]
                )
            else:
                sol[i_stock][cost] = sol[i_stock-1][cost]
    p = max_invest
    res = sol[n][p]
  
    for i in range(n,0,-1):
        if res == sol[i-1][p]:
            continue
        else:
            p = p - int(wallet.stocks[i-1].price)*100
            best_wallet.stocks.append(wallet.stocks[i-1])
            res = res - wallet.stocks[i-1].benefit*100
            if res < 0:
                break          

    return best_wallet

if __name__ == "__main__":
    all_stocks = Wallet(csv_file = "./data/dataset0.csv")
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    t1=time()
    best_wallet = optimized(all_stocks)
    t2=time()
    print(f"Function executed in {(t2-t1):.4f}s")
    print(best_wallet)