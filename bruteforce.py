import csv
from dataclasses import dataclass

csv_file = "data/dataset0.csv"

@dataclass
class Action:
    name: str
    price: float
    profit: float

def load_dataset() -> list:
    result = []
    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            action = Action(row['name'], float(row['price']), float(row['profit']))
            result.append(action)
    return result

if __name__ == '__main__':
    all_actions = load_dataset()
    print(all_actions)