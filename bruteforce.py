""" bruteforce_v4 + add wallet class """
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
    
def bruteforce(wallet: Wallet) -> Wallet:
    
    best_wallet = Wallet()
    maxbenef = 0
    n = len(wallet)

    # construction de 2**n combinaisons possibles
    # sous la forme d'une chaine de caractères
    # par exemple, pour 4 elements, la chaine 1010
    # dit que l'on sélectionne l'action 1 et l'action 3
    # 1111 si toutes les actions sont sélectionnées
    nb_combinaisons = 2**n
    for i in range(1, nb_combinaisons):
        # ecrit le rang sous forme binaire
        ch = bin(i)[2:]
        ch = (n - len(ch)) * "0" + ch

        # creer une liste d'actions sélectionnées
        ch = list(map(int, ch))  # ch en liste de 0 et 1

        current_wallet = Wallet()
        wallet_total_cost = 0
        for j, buy in enumerate(ch):
            if buy:
                if wallet_total_cost + wallet.stocks[j].price <= wallet.max_invest:
                    current_wallet.stocks.append(wallet.stocks[j])
                    wallet_total_cost += wallet.stocks[j].price
                else:
                    current_wallet.stocks=[]
                    wallet_total_cost = 0
                    break  # la combinaison est trop cher
       
        if maxbenef < current_wallet.totalbenef:
            maxbenef = current_wallet.totalbenef
            best_wallet = current_wallet

    return best_wallet


if __name__ == "__main__":
    all_stocks = Wallet(csv_file = "./data/dataset0.csv")
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    t1=time()
    best_wallet = bruteforce(all_stocks)
    t2=time()
    print(f"Function executed in {(t2-t1):.4f}s")
    print(best_wallet)