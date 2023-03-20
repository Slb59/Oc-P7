# Recursive. Try to turn this into a piece of top-down DP code.
def knapSack1(W : int, wt: list, val: list, n:int) -> int:
    """
    val =  values
    wt = weights
    n = number of items
    W = max capacity
    """ 
    if n == 0 or W == 0: 
        return 0; 

    if wt[n - 1] > W: 
        return knapSack1(W, wt, val, n - 1); 
    else:
        return max(val[n - 1] + knapSack1(W - wt[n - 1],  wt, val, n - 1), knapSack1(W, wt, val, n - 1)); 


def knapSack2(W: int, wt:list, val:list, n: int) : 
    
    i, w =0 
    K= [[0 for _ in range(n+1)] for _ in range(W+1)]

    for i in range(n+1): 
        for w in range(W+1): 
            if i == 0 or w == 0: 
                K[i][w] = 0; 
            elif (wt[i - 1] <= w): 
                K[i][w] = max( val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]); 
            else:
                K[i][w] = K[i - 1][w]; 
        
    return K[n][W]; 

if __name__ == '__main__':

    ...







