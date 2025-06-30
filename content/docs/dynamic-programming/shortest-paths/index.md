---
weight: 320
title: "Shortest Paths"
description: ""
icon: "article"
date: "2025-06-24T19:59:56+08:00"
lastmod: "2025-06-24T19:59:56+08:00"
draft: false
toc: true
katex: true
---

Given a directed graph `G` with weights on the edges, we define the **shortest path** between two vertices `i` and `j` as a path with the minimum total weight. The **all-pairs shortest path** problem is to find the shortest path between every pair of vertices in the graph.

{{< figure src="example.png" width="200px" class="text-center">}}

We use **dynamic programming** to solve this problem. The first step is to define a subproblem, after that derive a recursive formula. Using this formula, we can compute the value of the subproblem. Finally, we construct the optimal solution from the computed values.

## Subproblem

Let `G` be the input graph. We name the vertices in `G` by numbers, i.e. `V = [0, 1, ..., n-1]`. Consider any two vertices `i` and `j` in `V`, let `c[i, j]` be the length of edge `(i, j)`. Note that if there is no edge from `i` to `j`, then we set `c[i, j]` to infinity. Thus, we may assume w.l.o.g. that `G` is a complete graph.

Let `d(i, j, k)` be the shortest path length between `i` and `j`, whose **intermediate vertices** of the shortest path are drawn from `[1, ..., k-1]`. The **subproblem** is to compute `d(i, j, k)`, given `i`, `j` and `k`.

Note that `d(i, j, n)` returns the shortest path length between `i` and `j`. 

## Recursive Formula

Let `P` be the shortest path w.r.t. `d(i, j, k)`. Thus its intermediate vertices must be drawn from `[0, ..., k-1]`. We consider the last vertex from the set, i.e. `k-1`. There are two cases.

1. Vertex `k-1` is not in the intermediate vertices of `P`. In this case, `d(i, j, k) = d(i, j, k-1)`.
2. Vertex `k-1` is in the intermediate vertices of `P`. We can split `P` into two paths: `P_1 = (i, ..., k-1)` and `P_2 = (k-1, ..., j)`. Note that `P_1` and `P_2` are shortest paths, since `P` is the shortest path. Also, `k-1` is the last vertex in `P_1` and the first vertex in `P_2`. Thus, we have
$$
d(i, j, k) = d(i, k-1, k-1) + d(k-1, j, k-1)
$$

Summarizing, we have the following recursive formula:

$$
d(i, j, k) = \min\set{d(i, j, k-1),~ d(i, k-1, k-1) + d(k-1, j, k-1)}
$$

**Boundary Conditions**

If `k = 0`, it implies there is no intermediate vertices between `i` and `j`. In this case, the shortest path is the edge `(i, j)`. 

$$
d(i, j, 0) = c[i, j], \quad \forall i, j \in V
$$

## Solution

To construct the shortest paths, we use a table `p(i, j, k)` to store the shortest paths between `i` and `j` whose intermediate vertices are drawn from `[0, ..., k-1]`.

Initially, `p(i, j, 0)` is an empty list `[]` for all `i, j`.

Similar to the recursive formula, we have the following recursive formula for `p(i, j, k)`:

1. If `d(i, j, k) = d(i, j, k-1)`, then `p(i, j, k) = p(i, j, k-1)`.
2. If `d(i, j, k) = d(i, k-1, k-1) + d(k-1, j, k-1)`, then `p(i, j, k) = p(i, k-1, k-1) + [k-1] + p(k-1, j, k-1)`.

## Code

The dynamic programming algorithm for all pairs of shortest paths can implemented as below.

```python
import numpy as np
import copy


def shortest_paths(c):
    """ All-pairs of shortest paths
    :param c: cost matrix
        * c[i][j] = infinity if (i,j) not in E
        * c[i][j] = 0 if i = j
        * c[i][j] = cost from i to j, if (i,j) in E
    :return: distance matrix and shortest paths
    """
    n = len(c)
    # Shotrest path length
    d = np.full((n, n, n+1), np.inf)
    d[:, :, 0] = copy.copy(c)
    # Shortest paths
    p = np.empty((n, n, n+1), dtype=object)
    for i in range(n):
        for j in range(n):
            # Initialize shortest paths from i to j with length 0
            # The list contains the intermediate vertices in the shortest path
            p[i][j][0] = []

    for k in range(1, n+1):
        for i in range(n):
            for j in range(n):
                if d[i][j][k-1] > d[i][k-1][k-1] + d[k-1][j][k-1]:
                    d[i][j][k] = d[i][k-1][k-1] + d[k-1][j][k-1]
                    p[i][j][k] = p[i][k-1][k-1] + [k-1] + p[k-1][j][k-1]
                else:
                    d[i][j][k] = d[i][j][k-1]
                    p[i][j][k] = p[i][j][k-1]

    return d[:, :, n], p[:, :, n]
```

To see the result, we may define a function `print_paths` to print the shortest paths and their lengths.

```python
def print_paths(p, c):
    """
    :param p: shortest paths
    :param c: cost matrix
    """
    n = len(c)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            path = [i] + p[i][j] + [j]
            path_length = sum(c[path[k]][path[k+1]] for k in range(len(path)-1))
            print(f"({i}, {j}): path = {path}, length = {path_length}")
```

In addition, we define a function `random_instance` to generate a random instance of the problem.

```python

def random_instance(n):
    """
    :param n: number of nodes
    :return: random cost matrix
    """
    import numpy as np
    c = np.random.randint(1, 1000, (n, n))
    for i in range(n):
        c[i][i] = 0
    return c
    

if __name__ == '__main__':
    c = random_instance(10)
    p, _ = shortest_paths(c)
    print_paths(p, c)
```