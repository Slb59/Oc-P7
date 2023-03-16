import csv
from dataclasses import dataclass
from functools import wraps
from time import time

csv_file = "./data/dataset0.csv"

@dataclass
class Action:
    name: str
    price: float
    profit: float
    
    def benefice(self) -> float:
        return self.price * self.profit / 100

def timer_calc(func):
    """ time execution of a function """
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        t1=time()
        result = func(*args,  **kwargs)
        t2=time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrapper_function

def load_dataset() -> list:
    result = []
    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            action = Action(row['name'], float(row['price']), float(row['profit']))
            result.append(action)
    return result

def print_actions(dataset:list) -> None:
    for action in dataset:
        print(f"{action.name} prix:{action.price} benefice:{action.benefice()}")

def print_totalcost(dataset: list) -> None:
    print(f"Coût total: {sum(action.price for action in dataset)}")

def print_totalbenef(dataset: list) -> None:
    print(f"benefice total: {sum(action.benefice() for action in dataset)}")

@timer_calc
def bruteforce(dataset: list) -> list:
    result = []
    result.append(dataset[0])
    result.append(dataset[1])
    return result

if __name__ == '__main__':
    all_actions = load_dataset()
    print(f"Nombre d'actions en entrée: {len(all_actions)}")
    sel_actions = bruteforce(all_actions)
    print(f"Nombre d'actions en sortie: {len(sel_actions)}")
    print_actions(sel_actions)
    print_totalcost(sel_actions)
    print_totalbenef(sel_actions)