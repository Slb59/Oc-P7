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
    def benefice(self) -> float:
        return self.price * self.profit / 100
    
def load_dataset() -> list:
    result = []
    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            action = Action(row["name"], float(row["price"]), float(row["profit"]))
            result.append(action)
    return result

def print_actions(dataset: list) -> None:
    for action in dataset:
        print(f"{action.name} prix: {action.price} € benefice: {action.benefice} €")


def totalcost(dataset: list) -> float:
    return sum(action.price for action in dataset)


def totalbenef(dataset: list) -> float:
    return sum(action.benefice for action in dataset)


def print_totalcost(dataset: list) -> None:
    print(f"Coût total: {totalcost(dataset)} €")

def print_totalbenef(dataset: list) -> None:
    print(f"benefice total: {totalbenef(dataset):.2f} €")

def optimized(dataset: list) -> list:
    result = []
    maxbenef = 0
    n = len(dataset)
    ...
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
    print_actions(best_stocks)
    print("Résultats:")
    print_totalcost(best_stocks)
    print_totalbenef(best_stocks)