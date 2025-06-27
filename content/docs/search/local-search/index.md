---
weight: 230
title: "Local Search"
description: ""
icon: "article"
date: "2025-06-24T19:58:58+08:00"
lastmod: "2025-06-24T19:58:58+08:00"
draft: false
toc: true
katex: true
---

Local search is a simple but powerful algorithm. The basic idea is to start with a solution and then iteratively improve it. The improvement is done by trying out different moves. The move that results in the best improvement is chosen.

We use the traveling salesman problem (TSP) as an example to show the power of local search algorithm.

## TSP Problem

Given a complete graph `G = (V, E)` with edge weights `d(e)` for each edge `e ∈ E`. Each node represents a city and the edge weights represent the distances between cities. The TSP problem is to find the shortest route that visits all the cities exactly once. 

{{< figure src="tsp.png" width="300px" class="text-center">}}

## 2-OPT

Now we introduce a local search algorithm called `2-OPT` to solve the TSP problem. The algorithm is as follows:

1. Given a feasible initial solution $s$. Let us denote it by $s=\{(i_1, i_2), (i_2, i_3), \ldots, (i_n, i_1)\}$.
2. Define the neighborhood $\delta(s)$ of $s$: For any two arcs $(u, v)$ and $(s, t)$ in $s$, let us consider the solution $s'$ obtained by swapping their connections, i.e., $(u, s)$ and $(v, t)$. 
    {{< figure src="2opt.png" width="600px" class="text-center">}}
3. Search for $s'\in \delta(s)$, if $d(s') < d(s)$ (where $d(s)$ represents the total length of $s$), then take $s'$ as the new solution.
4. Stop when no improvement can be made or when the maximum number of iterations is reached.

* Example

{{< figure src="example.gif" width="600px" class="text-center">}}

## Code

```python
class TSP2opt(object):

    def __init__(self, d):
        """
        :param d: distance matrix
        """
        self._d = d
        self._iter = 0  # iteration count
        self._result = None
        self._result_length = 0
        self._tours = [] 

    def _init_tour(self):
        n = len(self._d)
        return [(i, i+1) for i in range(n-1)] + [(n-1, 0)]

    @staticmethod
    def _apply_2opt(tour, i, j):
        """ Apply 2opt to arc i and j.
        :param tour: list of arcs, e.g. tour of 4 vertices: [(0, 1), (1, 2), (2, 3), (3, 0)]
        :param i: arc i of the tour
        :param j: arc j of the tour.
        :return: a new tour (feasible solution)
        """
        u, v = tour[i]
        s, t = tour[j]
        part1 = tour[0:i]
        part2 = [(u, s)]
        part3 = [(tour[i+j-k][1], tour[i+j-k][0])for k in range(i+1, j)]
        part4 = [(v, t)]
        part5 = tour[j+1:]
        return part1 + part2 + part3 + part4 + part5

    def _is_2opt_make_improvement(self, tour, i, j):
        """
        Given a tour, assess whether applying 2opt(i,j) can make the tour shorter.
        """
        u, v = tour[i]
        s, t = tour[j]
        if self._d[u][v] + self._d[s][t] > self._d[u][s] + self._d[v][t]:
            return True
        return False

    def _get_tour_length(self, tour):
        return sum([self._d[i][j] for (i, j) in tour])

    def solve(self, max_iter=10000):
        n = len(self._d)
        self._result = self._init_tour()
        self._result_length = self._get_tour_length(self._result)
        self._tours.append(self._result)  # 记录中间结果

        improvement = 1
        while improvement >= 1:
            s0 = self._result_length
            for i in range(n):
                for j in range(i+1, n):
                    if self._iter == max_iter:
                        return self
                    if self._is_2opt_make_improvement(self._result, i, j):
                        self._result = self._apply_2opt(self._result, i, j)
                        self._tours.append(self._result) 
                        self._result_length = self._get_tour_length(self._result)
                        print("iter = %d, tour length = %d" %
                              (self._iter, self._get_tour_length(self._result)))
                        self._iter += 1
            improvement = self._result_length - s0

        return self

    def print_result(self):
        print("==== result ====")
        print("tour:", [arc[0] for arc in self._result])
        print("tour length:", self._result_length)

    def get_tours(self):
        return self._tours
```