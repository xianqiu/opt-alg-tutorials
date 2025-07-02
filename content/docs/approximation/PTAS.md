---
weight: 410
title: "PTAS"
description: ""
icon: "article"
date: "2025-06-24T19:32:51+08:00"
lastmod: "2025-06-24T19:32:51+08:00"
draft: false
toc: true
katex: true
---

PTAS is referred to as the **polynomial time approximation scheme**, which is a method to find a solution to a problem in polynomial time, with a guarantee that the solution is within a certain factor of the optimal solution.

We use the knapsack problem as an example to illustrate the approach.

## Knapsack Problem

Given $n$ items of weights $w_i$ and values $v_i$, for $i=0, 1, ..., n-1$ and a knapsack with a maximum weight capacity $C$, pack some items into the knapsack such that the total weight does not exceed $W$ and the total value of the packed items is maximized. 

## Algorithm

The algorithm has an input parameter $k$, which is a positive integer and is used to control the approximation ratio.

The algorithm is as follows:

1. Enumerate all possible subsets of items with at most $k$ items and total weight at most $C$. Find the subset $S$ with the maximum value.
2. Starting from $S$, fill the remaining capacities in a greedy way, i.e., sort the remaining items w.r.t. their value-to-weight ratio in non-increasing order, pack the items in this order until no item can be packed or the knapsack is full.

## Complexity

Enumerating all possible subsets of items with at most $k$ items and total weight at most $C$ takes time $O(2^k n)$. Sorting the remaining items takes time $O(n \log n)$. Filling the knapsack takes time $O(n)$.

Therefore, the total time complexity is $O(2^k n + n \log n + n) = O(n 2^k)$. As $k$ is a constant, this is a polynomial time algorithm.

Let `opt` be the optimal value of the knapsack problem and `alg` be the value of the solution found by the algorithm. 

It can be shown that the following holds:

$$
\text{opt} \leq \left(1 + \frac{1}{k}\right) \cdot \text{alg}
$$

In particular, for $k = 1$, the algorithm is a 2-approximation algorithm, i.e., the algorithm finds a value that is at least half of the optimal value.

From the above analysis, we can see that as $k$ increases, the approximation error decreases while the running time increases.

## Code

The first step is to enumerate all possible subsets of items with at most $k$ items. This is implemented by two functions.

* `choose_exact(n, k)`: from n items choose k items, enumerate all cases.
* `choose_at_most(n, k)`: from n items choose at most k items, enumerate all cases.

```python

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
```

Next we implement a na greedy algorithm for the knapsack problem. It will be used for filling the remaining capacities in the algorithm.

```python

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
```

Finally, the PTAS for the knapsack can be implemented as below.

```python

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
```