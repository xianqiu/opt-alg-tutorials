from ortools.linear_solver import pywraplp
import numpy as np


class MasterModel(object):

    def __init__(self, A, d):
        """
        :param A: 可行切割矩阵(每列代表一种切割方式)(m*n维矩阵),
                  其中m代表成品材料类型总数, n是我们考虑的可行切割方式的数量
        :param d: 成品材料的需求量(m维向量), m代表成品材料类型的总数
        """
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.CLP_LINEAR_PROGRAMMING)
        self._A = A
        self._d = d
        self._x = None  # 决策变量
        self._m, self._n = np.array(self._A).shape
        self._constraints = None  # 约束的集合(需要根据约束得到对偶变量, 别名shadow price)
        self._solution_x = None  # 计算结果
        self._sp = None  # shadow price(m维向量)

    def _init_decision_variables(self):
        self._x = [self._solver.NumVar(0, self._solver.Infinity(), "x[%d]" % j)
                   for j in range(self._n)]

    def _init_constraints(self):
        self._constraints = [None] * self._m
        for i in range(self._m):
            ct = self._solver.Constraint(self._d[i], self._d[i])
            for j in range(self._n):
                ct.SetCoefficient(self._x[j], self._A[i][j])
            self._constraints[i] = ct

    def _init_objective(self):
        obj = self._solver.Objective()
        for j in range(self._n):
            obj.SetCoefficient(self._x[j], 1)
        obj.SetMinimization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        self._solution_x = [self._x[j].solution_value() for j in range(self._n)]
        # shadow price
        self._sp = [self._constraints[i].dual_value() for i in range(self._m)]

    def print_info(self):
        print("[Master problem info]")
        print(" - Objective value =", self.get_objective_value())
        print(" - Shadow price: lambda = ", self._sp)

    def get_sp(self):
        """ 得到shadow price
        """
        return self._sp

    def get_solution(self):
        return self._solution_x

    def get_objective_value(self):
        return sum(self._solution_x)
