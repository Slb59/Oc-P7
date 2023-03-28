""" 
Load a csv dataset in a Wallet class and give a new wallet with
the best selection of stocks to optimize the final benefit

the bruteforce method is implemented

complexity : 2**n (n: number of stocks)
"""
import time
# from time import time
from wallet import Wallet
    
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
    t1=time.process_time()
    best_wallet = bruteforce(all_stocks)
    t2=time.process_time()
    print(f"Function executed in {(t2-t1):.4f}s")
    print(best_wallet)