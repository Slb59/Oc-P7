import csv
from dataclasses import dataclass


@dataclass
class Stock:
    """a stock has a name, a price, a profit and a benefit=price*profit/100"""

    name: str
    price: float
    profit: float

    @property
    def benefit(self) -> float:
        return self.price * self.profit / 100

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __hash__(self):
        return hash(("name", self.name))


class Wallet:
    """a wallet is a list of Stock
    all wallets have a max_invest"""

    max_invest = 500

    def __init__(self, csv_file=None) -> None:
        """a wallet can be init with a csv file
        the csv file need the columns name, price and profit"""
        self.stocks = []
        self.csv_file = csv_file

        if self.csv_file is not None:
            self.load_dataset()

    def __repr__(self) -> str:
        result = ""
        result += f"Actions du portefeuille: {len(self.stocks)}" + "\n"
        for stock in self.stocks:
            result += (
                f"{stock.name} prix: {stock.price} € benefice: {stock.benefit:.2f} €"
                + "\n"
            )
        result += "Valeur du portefeuille:" + "\n"
        result += f"Coût total: {self.totalcost:.2f} €" + "\n"
        result += f"Benefice sur 2 ans: {self.totalbenef:.2f} €" + "\n"
        return result

    def __len__(self):
        return len(self.stocks)

    @property
    def totalcost(self) -> float:
        """the totalcost is the sum of the price of the stocks in the wallet"""
        return sum(stock.price for stock in self.stocks)

    @property
    def totalbenef(self) -> float:
        """the totalbenef is the sum of the benef of the stocks in the wallet"""
        return sum(stock.benefit for stock in self.stocks)

    def load_dataset(self):
        """load the csv file without price <=0 or profit <=0
        or benefit minus 0.01 and remove duplicate stocks"""
        self.stocks = []
        with open(self.csv_file) as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                action = Stock(row["name"], float(row["price"]), float(row["profit"]))
                if (
                    action.price > 0
                    and action.profit > 0
                    and round(action.benefit, 0) > 0
                ):
                    self.stocks.append(action)
        # remove duplicate stock
        self.stocks = list(set(self.stocks))
        return self.stocks
