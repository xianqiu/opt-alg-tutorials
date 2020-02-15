from ortools.linear_solver import pywraplp
import numpy as np


class SudokuModel(object):

    def __init__(self, a):
        self._a = a
        self._x = None  # 决策变量
        self._solver = pywraplp.Solver('SudokuModel',
                                       pywraplp.Solver.BOP_INTEGER_PROGRAMMING)
        self._solution_x = None  # 计算结果

    def __init_decision_variables(self):
        self._x = np.empty((3, 3, 3, 3, 9)).tolist()
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        for n in range(9):
                            # x[i][j][p][q][n] >= a[i][j][p][q][n]
                            self._x[i][j][p][q][n] \
                                = self._solver.IntVar(self._a[i][j][p][q][n], 1,
                                                      'x[%d][%d][%d][%d][%d]' % (i, j, p, q, n))

    def __init_constraints(self):
        """
        # 已知数字不允许修改
        # x[i][j][p][q][n] >= a[i][j][p][q][n]
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        for n in range(9):
                            ct = self._solver.Constraint(self._a[i][j][p][q][n], self._solver.Infinity())
                            ct.SetCoefficient(self._x[i][j][p][q][n], 1)
        """
        # 一个单元格同时只允许填入一个数字
        # sum(x[i][j][p][q][n]) = 1, over n
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        ct = self._solver.Constraint(1, 1)
                        for n in range(9):
                            ct.SetCoefficient(self._x[i][j][p][q][n], 1)
        # 每个区块包含数字1-9
        # sum(x[i][j][p][q][n]) = 1, over p, q
        for i in range(3):
            for j in range(3):
                for n in range(9):
                    ct = self._solver.Constraint(1, 1)
                    for p in range(3):
                        for q in range(3):
                            ct.SetCoefficient(self._x[i][j][p][q][n], 1)
        # 每行包含数字1-9
        # sum(x[i][j][p][q][n]) = 1, over j, q
        for i in range(3):
            for p in range(3):
                for n in range(9):
                    ct = self._solver.Constraint(1, 1)
                    for j in range(3):
                        for q in range(3):
                            ct.SetCoefficient(self._x[i][j][p][q][n], 1)
        # 每列包含数字1-9
        # sum(x[i][j][p][q][n]) = 1, over i, p
        for j in range(3):
            for q in range(3):
                for n in range(9):
                    ct = self._solver.Constraint(1, 1)
                    for i in range(3):
                        for p in range(3):
                            ct.SetCoefficient(self._x[i][j][p][q][n], 1)

    def solve(self):
        self.__init_decision_variables()
        self.__init_constraints()
        self._solver.Solve()
        self._get_solution_x()

    def _get_solution_x(self):
        self._solution_x = np.empty((3, 3, 3, 3))
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        for n in range(9):
                            if self._x[i][j][p][q][n].solution_value() == 1:
                                self._solution_x[i][j][p][q] = n + 1

    def print_result(self):
        res = np.empty((9, 9))
        for i in range(3):
            for p in range(3):
                for j in range(3):
                    for q in range(3):
                        res[i*3+p][j*3+q] = self._solution_x[i][j][p][q]
        print(res)
