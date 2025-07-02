def choose_exact(n, k):
    """ from n items choose k items, enumerate all cases.
    >>> choose_exact(4, 2)
    [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    >>> choose_exact(3, 3)
    [[0, 1, 2]]
    """
    if k == 1:
        return [[i] for i in range(n)]
    res_mid = choose_exact(n, k - 1)
    result = []
    for p in res_mid:
        for i in range(max(p)+1, n):
            result.append(p + [i])
    return result


def choose_at_most(n, k):
    """ from n items choose at most k items, enumerate all cases.
    >>> choose_at_most(4, 2)
    [[], [0], [1], [2], [3], [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3], [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    """
    result = []
    for i in range(1, k+1):
        result += choose_exact(n, i)
    return result


def knapsack_greedy(w, v, C):
    """ Greedy algorithm for the knapsack problem. Return the indices of the packed items.
    >>> knapsack_greedy([1, 2, 3], [1, 3, 5], 4)
    [2, 0]
    """
    n = len(w)
    items = sorted(range(n), key=lambda i: v[i]/w[i], reverse=True)
    total_weight = 0
    packed_items = []
    for i in items:
        if total_weight + w[i] <= C:
            packed_items.append(i)
            total_weight += w[i]

    return packed_items


def knapsack_ptas(w, v, C, k):
    """ PTAS for the knapsack problem. Return the indices of the packed items.
    """
    # Step 1: Find the max subset with at most k items and total weight at most C.
    n = len(w)
    subsets = choose_at_most(n, k)
    max_value = 0
    max_subset = []
    for subset in subsets:
        total_weight = sum([w[i] for i in subset])
        total_value = sum([v[i] for i in subset])
        if total_weight <= C and total_value > max_value:
            max_value = total_value
            max_subset = subset
    
    # Step 2: Use the greedy algorithm to fill the remaining capacities.
    remaining_items = [i for i in range(n) if i not in max_subset]
    remaining_capacity = C - sum([w[i] for i in max_subset])
    packed_items = knapsack_greedy([w[i] for i in remaining_items], [v[i] for i in remaining_items], remaining_capacity)
    # Translate the indices of the packed items in Step 2 to the original indices.
    packed_items = [remaining_items[i] for i in packed_items]
    
    # Step 3: Combine the packed items in Step 1 and Step 2.
    return max_subset + packed_items


def print_items(items, w, v):
    print('Item Indices:', items)
    print('Total weight:', sum([w[i] for i in items]))
    print('Total value:', sum([v[i] for i in items]))


if __name__ == '__main__':
    w = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]
    v = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    C = 67
    # Optimal solution: [0, 3, 7], weight: 67, value: 1270
    # k >= 3 returns an optimal solution
    # k < 3 yields an approximate solution
    k = 3
    items = knapsack_ptas(w, v, C, k)
    print_items(items, w, v)