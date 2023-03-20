""" retrait de la class

Nombre d'actions en entrée: 20
Temps d'exécution: 20.3425s
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
from time import time


MAX_INVEST = 500
csv_file = "./data/dataset0.csv"


def load_dataset() -> tuple:
    stocks_name = []
    stocks_price = []
    stocks_profit = []
    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            stocks_name.append(row["name"])
            stocks_price.append(float(row["price"]))
            stocks_profit.append(float(row["profit"]))
    return (stocks_name, stocks_price, stocks_profit)


def print_actions(dataset: tuple) -> None:
    for i, action in enumerate(dataset[0]):
        print(f"{action} prix: {dataset[1][i]} € benefice: {dataset[1][i]*dataset[2][i]/100} €")


def totalcost(dataset: tuple) -> float:
    return sum(dataset[1][i] for i in range(len(dataset[0])))


def totalbenef(dataset: tuple) -> float:
    return sum(dataset[1][i]*dataset[2][i]/100 for i in range(len(dataset[0])))


def print_totalcost(dataset: tuple) -> None:
    print(f"Coût total: {totalcost(dataset)} €")


def print_totalbenef(dataset: tuple) -> None:
    print(f"benefice total: {totalbenef(dataset):.2f} €")

 
def bruteforce(dataset: tuple) -> tuple:
    result = []
    maxbenef = 0
    n = len(dataset[0])

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

        stock_list = [] # list of index
        stock_list_cost = 0
        for j, buy in enumerate(ch):
            if buy:
                if stock_list_cost + dataset[1][j] <= MAX_INVEST:
                    stock_list.append(j)
                    stock_list_cost += dataset[1][j]
                else:
                    stock_list = []
                    continue  # la combinaison est trop cher
        
        benef = sum(dataset[1][j]*dataset[2][j]/100 for j in stock_list)
        if maxbenef < benef:
            maxbenef = benef
            result = stock_list

    best_name = []
    best_price = []
    best_profit = [] 
    for i in result:
        best_name.append(dataset[0][i])
        best_price.append(dataset[1][i])
        best_profit.append(dataset[2][i])
    return (best_name, best_price, best_profit)


if __name__ == "__main__":
    all_stocks = load_dataset()
    print(f"Nombre d'actions en entrée: {len(all_stocks[0])}")
    t1=time()
    best_stocks = bruteforce(all_stocks)
    t2=time()
    print(f"Temps d'exécution: {(t2-t1):.4f}s")
    print(f"Nombre d'actions en sortie: {len(best_stocks[0])}")
    print("-----------------")
    print("Actions retenues:")
    print_actions(best_stocks)
    print("Résultats:")
    print_totalcost(best_stocks)
    print_totalbenef(best_stocks)