""" Premiers essais + test mode récursif (ne fonctionne pas)

Version liste binaire
Nombre d'actions en entrée: 20
Function 'bruteforce' executed in 959.9768s soit 0:15:59.976793
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


Version récursif:
Nombre d'actions en entrée: 20
Function executed in 13.7865s soit 0:00:13.786545
Nombre d'actions en sortie: 20
-----------------
Actions retenues:
Action-1 prix: 20.0 € benefice: 1.0 €
Action-2 prix: 30.0 € benefice: 3.0 €
Action-3 prix: 50.0 € benefice: 7.5 €
Action-4 prix: 70.0 € benefice: 14.0 €
Action-5 prix: 60.0 € benefice: 10.2 €
Action-6 prix: 80.0 € benefice: 20.0 €
Action-7 prix: 22.0 € benefice: 1.54 €
Action-8 prix: 26.0 € benefice: 2.86 €
Action-9 prix: 48.0 € benefice: 6.24 €
Action-10 prix: 34.0 € benefice: 9.18 €
Action-11 prix: 42.0 € benefice: 7.14 €
Action-12 prix: 110.0 € benefice: 9.9 €
Action-13 prix: 38.0 € benefice: 8.74 €
Action-14 prix: 14.0 € benefice: 0.14 €
Action-15 prix: 18.0 € benefice: 0.54 €
Action-16 prix: 8.0 € benefice: 0.64 €
Action-17 prix: 4.0 € benefice: 0.48 €
Action-18 prix: 10.0 € benefice: 1.4 €
Action-19 prix: 24.0 € benefice: 5.04 €
Action-20 prix: 114.0 € benefice: 20.52 €
Résultats:
Coût total: 822.0 €
benefice total: 130.06 €

"""

import csv
import logging
import sys
from dataclasses import dataclass
from functools import wraps
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


def timer_calc(func):
    """time execution of a function"""

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(
            f"Function {func.__name__!r} executed in {(t2-t1):.4f}s soit {timedelta(seconds=t2-t1)}"
        )
        return result

    return wrapper_function


def create_logger():
    logger = logging.getLogger("bruteforce")
    logger.setLevel(logging.DEBUG)
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("---> %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s " "- %(message)s", "%d/%m/%Y %H:%M:%S"
    )
    file_handler = logging.FileHandler("bruteforce.log", encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def load_dataset() -> list:
    logger.debug("load_dataset")
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

  

def bruteforce_rec(max_cost: int, dataset: list, n: int) -> list:
    if n == 0 or max_cost== 0:
        return dataset

    if dataset[n-1].price > max_cost:
        return bruteforce_rec(max_cost, dataset, n - 1)
    else:
        bf_last = bruteforce_rec(max_cost, dataset, n - 1)
        bf_prec = bruteforce_rec(max_cost - dataset[n-1].price, dataset, n - 1)
        if totalbenef(bf_last) > totalbenef(bf_prec):
            return bf_last
        else:
            return bf_prec


@timer_calc
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
        logger.debug("---")
        # ecrit le rang sous forme binaire
        ch = bin(i)[2:]
        ch = (n - len(ch)) * "0" + ch
        logger.debug(str(i) + ":" + ch)
        # creer une liste d'actions sélectionnées
        ch = list(map(int, ch))  # ch en liste de 0 et 1
        logger.debug(str(i) + ":" + str(ch))
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
        logger.debug(f"{str(stock_list)} : {str(benef)}")
        logger.debug(f"{str(result)} : {str(maxbenef)}")
    return result


if __name__ == "__main__":
    logger = create_logger()
    all_stocks = load_dataset()
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    best_stocks = bruteforce(all_stocks)
    #t1=time()
    #best_stocks = bruteforce_rec(MAX_INVEST, all_stocks, len(all_stocks))
    # t2=time()
    # print(
    #         f"Function executed in {(t2-t1):.4f}s soit {timedelta(seconds=t2-t1)}"
    #     )
    print(f"Nombre d'actions en sortie: {len(best_stocks)}")
    print("-----------------")
    print("Actions retenues:")
    print_actions(best_stocks)
    print("Résultats:")
    print_totalcost(best_stocks)
    print_totalbenef(best_stocks)
