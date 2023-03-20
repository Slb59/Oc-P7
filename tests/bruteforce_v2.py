""" retrait des logs et wrapper 
Nombre d'actions en entrée: 20
Temps d'exécution: 19.3582s = 0:00:19.358154
Nombre d'actions en sortie: 10
-----------------
Actions retenues:
Action-4 prix: 70.0 € benefice: 14.0 €
Action-5 prix: 60.0 € benefice: 10.2 €
Action-6 prix: 80.0 € benefice: 20.0 €
Action-8 prix: 26.0 € benefice: 2.86 €
Action-10 prix: 34.0 € benefice: 9.18 €
Action-11 prix: 42.0 € benefice: 7.14 €
Action-13 prix: 38.0 € benefice: 8.74 €
Action-18 prix: 10.0 € benefice: 1.4 €
Action-19 prix: 24.0 € benefice: 5.04 €
Action-20 prix: 114.0 € benefice: 20.52 €
Résultats:
Coût total: 498.0 €
benefice total: 99.08 €
"""

import csv
from dataclasses import dataclass
from time import time
from datetime import timedelta


MAX_INVEST = 500
csv_file = "./data/dataset0.csv"


@dataclass
class Action:
    name: str
    price: float
    profit: float

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
        print(f"{action.name} prix: {action.price} € benefice: {action.benefice()} €")


def totalcost(dataset: list) -> float:
    return sum(action.price for action in dataset)


def totalbenef(dataset: list) -> float:
    return sum(action.benefice() for action in dataset)


def print_totalcost(dataset: list) -> None:
    print(f"Coût total: {totalcost(dataset)} €")


def print_totalbenef(dataset: list) -> None:
    print(f"benefice total: {totalbenef(dataset):.2f} €")

 
def bruteforce(dataset: list) -> list:
    result = []
    maxbenef = 0
    n = len(dataset)

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

        stock_list = []
        stock_list_cost = 0
        for j, buy in enumerate(ch):
            if buy:
                if stock_list_cost + dataset[j].price <= MAX_INVEST:
                    stock_list.append(dataset[j])
                    stock_list_cost += dataset[j].price
                else:
                    stock_list = []
                    continue  # la combinaison est trop cher
        benef = totalbenef(stock_list)
        if maxbenef < benef:
            maxbenef = benef
            result = stock_list

    return result


if __name__ == "__main__":
    all_stocks = load_dataset()
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    t1=time()
    best_stocks = bruteforce(all_stocks)
    t2=time()
    print(f"Temps d'exécution: {(t2-t1):.4f}s = {timedelta(seconds=t2-t1)}")
    print(f"Nombre d'actions en sortie: {len(best_stocks)}")
    print("-----------------")
    print("Actions retenues:")
    print_actions(best_stocks)
    print("Résultats:")
    print_totalcost(best_stocks)
    print_totalbenef(best_stocks)
