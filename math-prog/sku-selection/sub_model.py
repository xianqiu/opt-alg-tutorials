from ortools.linear_solver import pywraplp
import numpy as np


class SubModel(object):
    """ 子问题i.
    """
    def __init__(self, pi, ci, y, bi):
        """ 下标i忽略
        :param pi: list, pi := p[i] = [p1, p2, ..., ]
        :param ci: list, ci := c[i] = [c1, c2, ..., ]
        :param y: scalar
        :param bi: scalar
        """
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self._pi = pi
        self._ci = ci
        self._y = y
        self._bi = bi
        self._x = None  # 决策变量
        self._solution_x = None  # 计算结果

    def _init_decision_variables(self):
        self._x = [None] * len(self._pi)
        for j in range(len(self._pi)):
            self._x[j] = self._solver.IntVar(0, 1, 'x[%d]' % j)

    def _init_constraints(self):
        ct = self._solver.Constraint(0, self._bi)
        for j in range(len(self._pi)):
            ct.SetCoefficient(self._x[j], 1)

    def _init_objective(self):
        obj = self._solver.Objective()
        for j in range(len(self._pi)):
            obj.SetCoefficient(self._x[j], self._pi[j] - self._y * self._ci[j])
        obj.SetMaximization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        self._solution_x = [s.solution_value() for s in self._x]

    def get_solution_x(self):
        return self._solution_x

    def get_obj_value(self):
        p = np.array(self._pi)
        c = np.array(self._ci)
        x = np.array(self._solution_x)
        return sum((p - self._y * c) * x)
