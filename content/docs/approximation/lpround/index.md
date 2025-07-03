---
weight: 430
title: "LP Rounding"
description: ""
icon: "article"
date: "2025-07-01T20:38:12+08:00"
lastmod: "2025-07-01T20:38:12+08:00"
draft: false
toc: true
katex: true
---

LP rounding is an approximation apporach for discrete optimization problems. It is a greedy algorithm that rounds the solution of the assoicated linear programming problem to the nearest integer.    

The algorithm works as follows:

1. Solve the linear programming problem and get the solution, say $x$.
2. For each variable $x_i$, round it to an integer and make sure it satisfies the constraints.

We use an example to illustrate this approach.

## Facility Location

Given a $m$ facilities and $n$ cities. Each facility $i$ has an openning cost $f_i$, and each city $j$ has a connection cost $c_{i,j}$, if $j$ is connnected to facility $i$. The problem is to determine a set of open facilities and to connect all cities, such that the total opening cost plus the total connection cost is minimized.

{{< figure src="facility-location.gif" width="400px" class="text-center">}}

The problem can be formulated as the following integer programming.

{{<katex>}}
$$
\begin{aligned}
\min~ & \sum_{i=1}^m f_i y_i + \sum_{i=1}^m \sum_{j=1}^n c_{i,j} x_{i,j} \\
\text{s.t. } & \sum_{i=1}^m x_{i,j} = 1, \quad \forall j\\
& x_{i, j}\leq y_i \quad \forall i, j\\
& x_{i,j}, y_i \in \{0, 1\}, \quad \forall i, j\\
\end{aligned}
$$
{{</katex>}}

We can uase an integer programming solver to solve this problem. Since the problem is NP-hard, for large instances, the problem may not solvabled in a reasonable time.

## Rounding 

An approximate approach is to solve the linear programming problem first, and then round the solution to an integer solution.

More specifically, the first step is to solve the following linear programming and get a fractional solution $x$ and $y$.

{{<katex>}}
$$
\begin{aligned}
\min~ & \sum_{i=1}^m f_i y_i + \sum_{i=1}^m \sum_{j=1}^n c_{i,j} x_{i,j} \\
\text{s.t. } & \sum_{i=1}^m x_{i,j} = 1, \quad \forall j\\
& x_{i, j}\leq y_i \quad \forall i, j\\
& x_{i,j}, y_i \geq 0, \quad \forall i, j\\
\end{aligned}
$$
{{</katex>}}

The second step is to round $y_i$ to its nearest integer for all $i$. Finally, connect the cities to their nearest facility, i.e., let $x_{i,j} = 1$ if $y_i = 1$ and $c_{i,j}$ is the smallest among all $c_{i,j}$ such that $y_i = 1$.

## Code

The first step is to use a linear programming solver to solve the problem. We use the open-source solver [OR-Tools](https://developers.google.com/optimization) in this example.

```python
from ortools.linear_solver import pywraplp


def facility_location_lp(f, c):
    """
    Use ortools to solve the "relaxed" facility location problem.
    """
    m, n = c.shape
    # Create the linear solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        raise Exception("Solver not created.")

    # Variables
    x = [[solver.NumVar(0, 1, f'x[{i}][{j}]') for j in range(n)] for i in range(m)]
    y = [solver.NumVar(0, 1, f'y[{i}]') for i in range(m)]
    
    # Constraints
    # Each customer is assigned to exactly one facility
    for j in range(n):
        solver.Add(solver.Sum(x[i][j] for i in range(m)) == 1)
    # Customers can only be assigned to open facilities
    for i in range(m):
        for j in range(n):
            solver.Add(x[i][j] <= y[i])

    # Objective: minimize total cost
    objective = solver.Sum(f[i] * y[i] for i in range(m)) + solver.Sum(c[i][j] * x[i][j] for i in range(m) for j in range(n))
    solver.Minimize(objective)

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        raise Exception("The problem does not have an optimal solution.")

    # Extract solution
    y_sol = [y[i].solution_value() for i in range(m)]
    x_sol = [[x[i][j].solution_value() for j in range(n)] for i in range(m)]

    return x_sol, y_sol
```

Now the algorithm can be implemented as below.
```python
import numpy as np


def facility_location_lp_rounding(f, c):
    """
    Use LP rounding approach to solve the facility location problem.
    """
    x, y = facility_location_lp(f, c)
    y = np.round(y)
    # Connect city j to the facility with the smallest distance
    for j in range(c.shape[1]):
        min_index = np.argmin(c[:, j])
        x[min_index][j] = 1
    
    return x, y
```

For ease of showing the result, we also implement a function to print the solution.

```python

def print_solution(x, y, f, c):
    """
    Print the solution to the facility location problem.
    """
    opening_cost = sum(f[i] * y[i] for i in range(len(y)))
    connection_cost = sum(c[i][j] * x[i][j] for i in range(len(y)) for j in range(len(x[i])))
    print("-------------------------")
    print("Total Cost: ", opening_cost + connection_cost)
    print("-------------------------")
    for i in range(len(y)):
        if y[i] == 1:
            print(f"Facility {i}: opening cost = {f[i]}")
            connected_cities = [j for j in range(len(x[i])) if x[i][j] == 1]
            print(f"|-- Connected cities: {connected_cities}, cost = {sum(c[i][j] for j in connected_cities)}")
```
