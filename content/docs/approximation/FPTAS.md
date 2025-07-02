---
weight: 420
title: "FPTAS"
description: ""
icon: "article"
date: "2025-06-24T19:32:55+08:00"
lastmod: "2025-06-24T19:32:55+08:00"
draft: false
toc: true
katex: true
---

FPTAS is referred to as the **fully polynomial time approximation scheme**, which is a method to find a solution to a problem in polynomial time, with a guarantee that the solution is within a certain factor of the optimal solution.

Compared to [PTAS](/docs/approximation/ptas), the FPTAS is more efficient in time complexity. Given a small constant $\epsilon > 0$, the running time of FPTAS is polynomial in $1/\epsilon$, while the PTAS is exponential in $1/\epsilon$. 

We use the knapsack problem as an example to illustrate this approch. 

## Knapsack Problem

Given $n$ items of weights $w_i$ and values $v_i$, for $i=0, 1, ..., n-1$ and a knapsack with a maximum weight capacity $C$, pack some items into the knapsack such that the total weight does not exceed $W$ and the total value of the packed items is maximized. Assume that the weights, the values and the capacity are all integers.

## Algorithm

The FPTAS algorithm for the knapsack problem is as follows:

1. Round the instance by scaling the values of the items w.r.t. a given factor $\epsilon > 0$.

    Let $K = \frac{\epsilon V}{n}$, where $V= \max\set{v_i}$. The new instance is obtained by scaling $v_i$ to 
    $$v'_i = \lfloor v_i/K  \rfloor
    \quad \forall i=0, 1, ..., n-1.$$

2. Solve the scaled knapsack problem using a polynomial-time algorithm, such as the dynamic programming algorithm.

## Dynamic Programming

Let $f(i, s)$ be the minimum weight of items with a total value of at least $s$, drawn from the item set $\set{0, 1, ..., i-1}$

Consider the last item $i-1$. There are three cases:

1. If $v_{i-1} > s$, then $i-1$ cannot be packed, then $f(i, s) = f(i-1, s)$. 
2. If $v_{i-1} \leq s$ and $i-1$ is packed, then $f(i, s) = f(i-1, s - v_{i-1}) + w_{i-1}$
3. If $v_{i-1} \leq s$ and $i-1$ is not packed, then $f(i, s) = f(i-1, s)$.

Summarizing, the optimal substructure of the problem is as follows:
{{<katex>}}
$$
f(i, s) = \begin{cases}
    \min\set{f(i-1, s), f(i-1, s-v_{i-1}) + w_{i-1}} & \text{if } v_{i-1} \leq s\\
    f(i-1, s) & \text{if } v_{i-1} > s
\end{cases}
$$
{{</katex>}}

For $s = \sum_{i=0}^{n-1} v_i, ..., 0$, the optimal value of the problem is to find the maximum $s$ such that $f(n, s) \leq C$.

**Initial Conditions**

Note that $f$ takes the minimum value of the two cases, so we initialize $f(i, s)$ to $\infty$ by default, except for two special cases.

The first one is $f(1, v_0)$, in this case items are drawn from the singleton set $\set{0}$, thus the optimal value is $w_0$.

The second one is $f(i, 0) = 0$, in this case no items should be packed into the knapsack, so the optimal value is $0$.

Summarizing, we have the following initial conditions.

{{<katex>}}
$$
f(i, s) = \begin{cases}
    w_0, & \text{if } i=1, s=v_0 \\
    0, & \text{if } s=0 \\
    \infty, &  \text{else}
\end{cases}
$$
{{</katex>}}

## Code

The first step is to implement the above dynamic programming algorithm for the knapsack problem.

```python
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
```

The FPTAS for the knapsack problem can be implemented as below.

```python

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
```

## Complexity

Let `opt` be the optimal value of the knapsack problem and `alg` be the value of the solution found by the algorithm. Given $\epsilon > 0$, it can be shown that the following holds:

{{<katex>}}
$$
\text{alg} \geq (1 - \epsilon) \cdot \text{opt}
$$
{{</katex>}}

Now we look at the running time of the FPTAS algorithm. 

Note that the dynimic programming runs in $O(n^2 \cdot nV)$, where $V$ is the maximal value of the items. In the FPTAS, we round the values to $\lfloor v_i / K \rfloor$, thus the running time of the FPTAS is 

$$O(n^2 \cdot \lfloor V/K\rfloor) = O(n^2 \cdot \lfloor n/\epsilon \rfloor).$$
