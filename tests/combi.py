import itertools
if __name__ == '__main__':
    data = [1, 2, 3]
    
    for i in range(1, len(data)+1):
        for subset in itertools.combinations(data,i):
            print(subset)
