---
weight: 310
title: "Knapsack"
description: ""
icon: "article"
date: "2025-06-24T19:59:46+08:00"
lastmod: "2025-06-24T19:59:46+08:00"
draft: true
toc: true
katex: true
---

Given $n$ items of weights $w_i$ and values $v_i$, for $i=0, 1, ..., n-1$ and a knapsack with a maximum weight capacity $C$, pack some items into the knapsack such that the total weight does not exceed $W$ and maximize the total value of the packed items. Assume that the weights, the values and the capacity are all integers.

The problem is a classic example of the **dynamic programming** approach. The key idea is to break down the problem into smaller subproblems and store the solutions to these subproblems to avoid recomputation.

## Subproblem

Let $f(i, s)$ be the maximum value that can be obtained by packing items from $\set{1, ..., i-1}$ into a knapsack with a capacity of $s$.

The subproblem is to compute $f(i, s)$ for $i=1, ..., n$ and $s=1, 2, ..., C$. The maximum value is $f(n-1, C)$.

## Recursive formula

To compute $f(i, s)$, consider the last item $i-1$. There are three cases:

1. If $w_{i-1} > s$, then $i-1$ is not packed into the knapsack, the maximum value is $f(i-1, s)$.
2. If $s\geq w_{i-1}$ and $i-1$ is packed into the knapsack, then the maximum value is $f(i-1, s-w_{i-1}) + v_{i-1}$. 
3. If $s\geq w_{i-1}$ and $i-1$ is not packed into the knapsack, then the maximum value is $f(i-1, s)$.

Summarizing, we have the following recurrence relation:
{{<katex>}}
$$
f(i, s) = \begin{cases}
f(i-1, s), & s<w_{i-1} \\
\max\set{f(i-1, s), f(i-1, s-w_{i-1}) + v_{i-1}}, & s\geq w_{i-1}
\end{cases}
$$
{{</katex>}}

**Initial Conditions**

In order to compute the recursive formula, we need initial conditions. It is easy to see that the following conditions hold.

$f(0, s) = 0$ for $s=1, 2, ..., C$.

## Implementation

We can use **bottom-up** or **top-down with memoization** to implement the dynamic programming algorithm. 

From my perspective, bottom-up is easier to implement. As it is not recursive, it is convenient to check the logic and see the intermediate results.

The following is a bottom-up implementation.

```python

def knapsack_value(w, v, C):
    """
    :param w: list of weights
    :param v: list of values
    :param C: capacity
    :return: maximum value
    """
    n = len(w)
    f = [[0 for _ in range(C+1)] for _ in range(n)]
    for i in range(1, n):
        for s in range(1, C+1):
            if w[i-1] > s:
                f[i][s] = f[i-1][s]
            else:
                f[i][s] = max(f[i-1][s], f[i-1][s-w[i-1]] + v[i-1])
    return f[n-1][C]
```

## Solution

Note that the above implementation only returns the maximum value. In order to construct the optimal solution, we need to store the information about which item is packed into the knapsack. 

We can use value table $f$ to construct the solution. If $f(i, s) = f(i-1, s-w_i) + v_i$, then item $i$ is packed into the knapsack, and the remaining capacity is $s-w_i$. Otherwise, item $i$ is not packed into the knapsack. 

By integrating this step into the algorithm described above, we can obtain the optimal solution.

```python

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
    # Construct the solution
    packed_items = []
    s = C
    for i in range(n, 0, -1):
        if f[i][s] != f[i - 1][s]: 
            packed_items.append(i - 1) 
            s -= w[i - 1]
    packed_items.reverse()
    
    return f[n][C], packed_items
```

