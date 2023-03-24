"""
Nombre d'actions en entrée: 20
Temps d'exécution: 0.0000s
Nombre d'actions en sortie: 12
-----------------
Actions retenues:
Action-10 prix: 34.0 € benefice: 9.18 €
Action-6 prix: 80.0 € benefice: 20.0 €
Action-13 prix: 38.0 € benefice: 8.74 €
Action-19 prix: 24.0 € benefice: 5.04 €
Action-4 prix: 70.0 € benefice: 14.0 €
Action-20 prix: 114.0 € benefice: 20.52 €
Action-5 prix: 60.0 € benefice: 10.2 €
Action-11 prix: 42.0 € benefice: 7.14 €
Action-18 prix: 10.0 € benefice: 1.4 €
Action-17 prix: 4.0 € benefice: 0.48 €
Action-16 prix: 8.0 € benefice: 0.64 €
Action-14 prix: 14.0 € benefice: 0.14 €
Résultats:
Coût total: 498.0 €
benefice total: 97.48 €
"""

import csv
from dataclasses import dataclass
from time import time


MAX_INVEST = 500
csv_file = "./data/dataset0.csv"


@dataclass
class Action:
    name: str
    price: float
    profit: float

    @property
    def benefit(self) -> float:
        return self.price * self.profit / 100
    
def load_dataset() -> list:
    result = []
    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            action = Action(row["name"], float(row["price"]), float(row["profit"]))
            result.append(action)
    return result

def print_stocks(dataset: list) -> None:
    for action in dataset:
        print(f"{action.name} prix: {action.price} € benefice: {action.benefit} €")


def totalcost(dataset: list) -> float:
    return sum(action.price for action in dataset)


def totalbenef(dataset: list) -> float:
    return sum(action.benefit for action in dataset)


def print_totalcost(dataset: list) -> None:
    print(f"Coût total: {totalcost(dataset)} €")

def print_totalbenef(dataset: list) -> None:
    print(f"benefice total: {totalbenef(dataset):.2f} €")

def optimized(dataset: list) -> list:
    result = []
    stock_list_cost = 0
    # sort dataset by reverse profit
    sorted_dataset = sorted(dataset, key=lambda stock: stock.profit, reverse=True)
    for stock in sorted_dataset:
        if stock.price + stock_list_cost <= MAX_INVEST:
            stock_list_cost += stock.price
            result.append(stock)
        if stock_list_cost == MAX_INVEST:
            break
    return result

if __name__ == "__main__":
    all_stocks = load_dataset()
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    t1 = time()
    best_stocks = optimized(all_stocks)
    t2 = time()
    print(f"Temps d'exécution: {(t2-t1):.4f}s")
    print(f"Nombre d'actions en sortie: {len(best_stocks)}")
    print("-----------------")
    print("Actions retenues:")
    print_stocks(best_stocks)
    print("Résultats:")
    print_totalcost(best_stocks)
    print_totalbenef(best_stocks)