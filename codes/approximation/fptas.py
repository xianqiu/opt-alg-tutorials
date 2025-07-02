import numpy as np


def knapsack_dp(w, v, C):
    """
    Dynamic programming solution to the knapsack problem.
    :param w: list of weights
    :param v: list of values
    :param C: capacity
    :return: maximum value, list of items (indices)
    """
    n = len(w)
    m = sum(v)
    # Initial conditions
    f = np.full((n+1, m + 1), np.inf)
    f[:, 0] = 0
    f[1][v[0]] = w[0]
    # Compute the table
    for i in range(n + 1):
        for s in range(m + 1):
            if v[i - 1] <= s:
                f[i][s] = min(f[i - 1][s], f[i - 1][s - v[i - 1]] + w[i - 1])
            else:
                f[i][s] = f[i - 1][s]

    max_value = 0
    for s in range(m, -1, -1):
        if f[n][s] <= C:
            max_value = s
            break
    
    # Construct the solution
    packed_items = []
    for i in range(n, 0, -1):
        if f[i][s] != f[i - 1][s]:
            packed_items.append(i - 1)
            s -= v[i - 1]
    packed_items.reverse()
    
    return max_value, packed_items


def knapsack_fptas(w, v, C, eps):
    """
    :param w: list of weights
    :param v: list of values
    :param C: capacity
    :param eps: error tolerance
    :return: list of items (indices)
    """
    # Step1: Round values 
    n = len(w)
    V = sum(v)
    K = eps * V / n
    v1 = [int(v[i] / K) for i in range(n)]
    # Step2: Solve knapsack w.r.t. v1
    _, items = knapsack_dp(w, v1, C)

    return items


def print_items(items, w, v):
    print('Item Indices:', items)
    print('Total weight:', sum([w[i] for i in items]))
    print('Total value:', sum([v[i] for i in items]))


if __name__ == '__main__':
    w = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]
    v = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    C = 67
    eps = 0.1
    items = knapsack_fptas(w, v, C, eps) 
    print_items(items, w, v)