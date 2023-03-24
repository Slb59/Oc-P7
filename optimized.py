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
    stock_list_cost = 0
    # sort dataset by reverse profit
    sorted_dataset = sorted(wallet.stocks, key=lambda stock: stock.profit, reverse=True)
    for stock in sorted_dataset:
        if stock.price + stock_list_cost <= wallet.max_invest:
            stock_list_cost += stock.price
            best_wallet.stocks.append(stock)
        if stock_list_cost == wallet.max_invest:
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