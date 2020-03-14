from ortools.linear_solver import pywraplp
import numpy as np


class SubModel(object):

    def __init__(self, y, C):
        """
        :param y: 主问题的解(代表y_i=1代表开设仓i)
        :param C: 连接成本(m*n维矩阵)
        """
        self._solver = pywraplp.Solver('SubModel',
                                       pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        self._y = y
        self._c = C
        self._m = len(self._c)
        self._n = len(self._c[0])
        self._alpha = None  # 决策变量
        self._beta = None  # 决策变量
        self._constraints = []  # 所有约束(后续获取对偶变量, 得到原始问题的解)
        self._solution_alpha = None  # 计算结果
        self._solution_beta = None  # 计算结果

    def _init_decision_variables(self):
        self._alpha = [self._solver.NumVar(-self._solver.Infinity(),
                                           self._solver.Infinity(),
                                           'alpha[%d]' % j)
                       for j in range(self._n)]

        self._beta = [[self._solver.NumVar(0, self._solver.Infinity(), 'beta[%d][%d]' % (i, j))
                      for j in range(self._n)] for i in range(self._m)]

    def _init_constraints(self):
        for i in range(self._m):
            self._constraints.append([])
            for j in range(self._n):
                ct = self._solver.Constraint(-self._solver.Infinity(), self._c[i][j])
                ct.SetCoefficient(self._alpha[j], 1)
                ct.SetCoefficient(self._beta[i][j], -1)
                self._constraints[i].append(ct)

    def _init_objective(self):
        obj = self._solver.Objective()
        for j in range(self._n):
            obj.SetCoefficient(self._alpha[j], 1)
        for i in range(self._m):
            for j in range(self._n):
                obj.SetCoefficient(self._beta[i][j], -self._y[i])

        obj.SetMaximization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        self._solution_alpha = [self._alpha[j].solution_value() for j in range(self._n)]
        self._solution_beta = [[self._beta[i][j].solution_value()
                                for j in range(self._n)]
                               for i in range(self._m)]

    def get_solution(self):
        return self._solution_alpha, self._solution_beta

    def get_objective_value(self):
        return sum(self._solution_alpha) - sum(np.array(self._y) * np.sum(self._solution_beta, axis=1))

    def get_dual_values(self):
        """ 得到原问题的解: x[i][j]
        """
        return [[self._constraints[i][j].dual_value()
                for j in range(self._n)]
                for i in range(self._m)]
