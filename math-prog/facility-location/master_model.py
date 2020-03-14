from ortools.linear_solver import pywraplp

import numpy as np


class MasterModel(object):

    def __init__(self, f, fix_z=None):
        """
        :param f: 开仓成本(m维向量)
        :param fix_z: 限定z的值. 目的是初始化的时候令z=0,然后求解主问题得到y的值.
        """
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        self._f = f
        self._fix_z = fix_z
        self._m = len(self._f)
        self._y = None  # 决策变量
        self._z = None  # 决策变量
        self._solution_y = None  # 计算结果
        self._solution_z = None  # 计算结果
        # 迭代求解之前会调用add_constraint
        # 所以决策变量的初始化要放在前面
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()

    def _init_decision_variables(self):
        self._y = [self._solver.NumVar(0, 1, 'y[%d]' % i)
                   for i in range(self._m)]
        self._z = self._solver.NumVar(-self._solver.Infinity(), self._solver.Infinity(), 'z')

    def _init_objective(self):
        obj = self._solver.Objective()
        for i in range(self._m):
            obj.SetCoefficient(self._y[i], self._f[i])
        obj.SetCoefficient(self._z, 1)
        obj.SetMinimization()

    def add_constraint(self, alpha, beta):
        """ Benders主流程会调用此方法为主问题增加新的约束.

        :param alpha: 子问题的解
        :param beta: 子问题的解
        """
        ct = self._solver.Constraint(sum(alpha), self._solver.Infinity())
        for i in range(self._m):
            ct.SetCoefficient(self._y[i], sum(beta[i]))
        ct.SetCoefficient(self._z, 1)

    def _init_constraints(self):
        if self._fix_z is not None:
            ct = self._solver.Constraint(self._fix_z, self._fix_z)
            ct.SetCoefficient(self._z, 1)

        ct = self._solver.Constraint(1, self._solver.infinity())
        for i in range(self._m):
            ct.SetCoefficient(self._y[i], 1)

    def solve(self):
        self._solver.Solve()
        self._solution_y = [self._y[i].solution_value() for i in range(self._m)]
        self._solution_z = self._z.solution_value()

    def get_solution(self):
        return self._solution_y, self._solution_z

    def get_objective_value(self):
        return sum(np.array(self._solution_y) * np.array(self._f)) + self._solution_z

