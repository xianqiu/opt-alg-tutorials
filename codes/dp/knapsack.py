import numpy as np


def knapsack_value(w, v, C):
    """
    :param w: list of weights
    :param v: list of values
    :param C: capacity
    :return: maximum value
    """
    n = len(w)
    f = [[0 for _ in range(C+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for s in range(1, C+1):
            if w[i-1] > s:
                f[i][s] = f[i-1][s]
            else:
                f[i][s] = max(f[i-1][s], f[i-1][s-w[i-1]] + v[i-1])
    return f[n][C]


def knapsack(w, v, C):
    """
    :param w: list of weights
    :param v: list of values
    :param C: capacity
    :return: total value, list of items (indices)
    """
    n = len(w)
    f = [[0 for _ in range(C+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for s in range(1, C+1):
            if w[i-1] > s:
                f[i][s] = f[i-1][s]
            else:
                f[i][s] = max(f[i-1][s], f[i-1][s-w[i-1]] + v[i-1])

    packed_items = []
    s = C
    for i in range(n, 0, -1):
        if f[i][s] != f[i - 1][s]: 
            packed_items.append(i - 1) 
            s -= w[i - 1]
    packed_items.reverse()
    
    return f[n][C], packed_items


def print_items(items, w, v):
    print('Item Indices:', items)
    print('Total weight:', sum([w[i] for i in items]))
    print('Total value:', sum([v[i] for i in items]))


if __name__ == '__main__':
    w = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]
    v = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    C = 67
    f, items = knapsack(w, v, C) 
    print_items(items, w, v)
 