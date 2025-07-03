import numpy as np
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
            
        
if __name__ == '__main__':
    # Generate random data
    m = 10
    n = 20
    f = np.random.randint(1, 10, size=m)
    c = np.random.randint(1, 100, size=(m, n))
    x, y = facility_location_lp_rounding(f, c)
    print_solution(x, y, f, c)

