from ortools.linear_solver import pywraplp
import numpy as np


class CheckModel(object):
    """ 直接求解设施选址问题.
    检查Benders分解的计算结果是否正确.
    """

    def __init__(self, f, C):
        self._f = f
        self._c = C
        self._m = len(f)
        self._n = len(C[0])
        self._solver = pywraplp.Solver('CheckModel',
                                       pywraplp.Solver.CLP_LINEAR_PROGRAMMING)
        self._y = None
        self._x = None

        self._init_variables()  #
        self._init_objective()

    def _init_variables(self):
        self._y = [self._solver.NumVar(0, 1, 'y[%d]' % i)
                   for i in range(self._m)]

        self._x = [[self._solver.NumVar(0, self._solver.Infinity(), 'x[%d][%d]' % (i, j))
                    for j in range(self._n)] for i in range(self._m)]

    def _init_constraints(self):
        for j in range(self._n):
            ct = self._solver.Constraint(1, 1)
            for i in range(self._m):
                ct.SetCoefficient(self._x[i][j], 1)
        for i in range(self._m):
            for j in range(self._n):
                ct = self._solver.Constraint(0, self._solver.Infinity())
                ct.SetCoefficient(self._y[i], 1)
                ct.SetCoefficient(self._x[i][j], -1)

    def _init_objective(self):
        self._obj = self._solver.Objective()
        for i in range(self._m):
            self._obj.SetCoefficient(self._y[i], self._f[i])
            for j in range(self._n):
                self._obj.SetCoefficient(self._x[i][j], self._c[i][j])
        self._obj.SetMinimization()

    def solve(self):
        self._init_constraints()

        self._solver.Solve()
        solution_x = [[self._x[i][j].solution_value()
                      for j in range(self._n)]
                      for i in range(self._m)]
        solution_y = [self._y[i].solution_value() for i in range(self._m)]

        fy = np.sum(np.array(solution_y) * np.array(self._f))
        fx = np.sum(np.array(solution_x) * np.array(self._c))
        obj = fx + fy

        print("optimal solution value:", obj)
        print("y =", solution_y)


if __name__ == '__main__':
    from gen_data import f, C
    CheckModel(f, C).solve()
