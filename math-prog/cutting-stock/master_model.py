from ortools.linear_solver import pywraplp
import numpy as np


class MasterModel(object):

    def __init__(self, A, d):
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.CLP_LINEAR_PROGRAMMING)
        self._A = A
        self._d = d
        self._x = None  # 决策变量
        self._m, self._n = np.array(self._A).shape
        self._constraints = None  # 约束的集合(用来获取shadow price)
        self._solution_x = None  # 计算结果
        self._obj = None
        self._la = None  # shadow price(m维向量)

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
        self._obj = self._solver.Objective()
        for j in range(self._n):
            self._obj.SetCoefficient(self._x[j], 1)
        self._obj.SetMinimization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        self._solution_x = [self._x[j].solution_value() for j in range(self._n)]
        self._la = [self._constraints[i].dual_value() for i in range(self._m)]  # shadow price
        self._obj = sum(self._solution_x)

    def print_info(self):
        print("[Master problem info]")
        print(" - Objective value =", self._obj)
        print(" - Shadow price: lambda = ", self._la)

    def get_la(self):
        return self._la

    def get_solution(self):
        return self._solution_x

    def get_objective_value(self):
        return self._obj
