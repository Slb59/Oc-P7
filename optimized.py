"""
Load a csv dataset in a Wallet class and give a new wallet with
the best selection of stocks to optimize the final benefit

the dynamic programming method is implemented
the greedy algorithm is proposed
"""

import time
from wallet import Wallet


def optimized_greedy(wallet: Wallet) -> Wallet:
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


def optimized_dynamic(wallet: Wallet) -> Wallet:
    wallet.stocks = sorted(wallet.stocks, key=lambda stock: stock.profit, reverse=True)
    best_wallet = Wallet()
    n = len(wallet)
    max_invest = int(wallet.max_invest * 100)

    sol = [[0 for _ in range(max_invest + 1)] for _ in range(n + 1)]

    # first line : 0 stock is tested
    # last line : the nieme stock is tested
    for i_stock in range(1, n + 1):
        price_stock = int(
            wallet.stocks[i_stock - 1].price * 100
        )  # line i_stock is the stock i_stock-1

        for cost in range(1, max_invest + 1):
            if price_stock <= cost:
                # if the price of the action is less than the wallet cost
                # the value of the cell is the max between the benefit of the action
                # + the value of the cell in the same row but with the wallet value -
                # the value of the action and the value of the cell in the row above
                sol[i_stock][cost] = max(
                    int(wallet.stocks[i_stock - 1].benefit * 100)
                    + sol[i_stock - 1][cost - price_stock],
                    sol[i_stock - 1][cost],
                )
            else:
                sol[i_stock][cost] = sol[i_stock - 1][cost]

    p = max_invest

    while p >= 0 and n >= 0:
        stock = wallet.stocks[n - 1]
        if sol[n][p] == sol[n - 1][p - int(stock.price * 100)] + int(
            stock.benefit * 100
        ):
            best_wallet.stocks.append(stock)
            p -= int(stock.price * 100)
        n -= 1

    return best_wallet


if __name__ == "__main__":
    all_stocks = Wallet(csv_file="./data/dataset0.csv")
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    t1 = time.process_time()
    best_wallet = optimized_dynamic(all_stocks)
    t2 = time.process_time()
    print(f"Function executed in {(t2-t1):.4f}s")
    print(best_wallet)

    all_stocks = Wallet(csv_file="./data/dataset0.csv")
    print(f"Nombre d'actions en entrée: {len(all_stocks)}")
    t1 = time.process_time()
    best_wallet = optimized_greedy(all_stocks)
    t2 = time.process_time()
    print(f"Function executed in {(t2-t1):.4f}s")
    print(best_wallet)
