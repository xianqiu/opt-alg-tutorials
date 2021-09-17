from ortools.linear_solver import pywraplp
import numpy as np


class CutPlane(object):
    """ 割平面法。
    注意：
    1、最大化问题（约束形式为 Ax <= b）。
    2、整数规划。
    3、决策变量非负。
    """

    def __init__(self, c, A, b, lb=None, ub=None):
        """
        :param c: n * 1 vector
        :param A: m * n matrix
        :param b: m * 1 vector
        :param lb: list, lower bounds of x, e.g. [0, 0, 1, ...]
        :param ub: list, upper bounds of x, e.g. [None, None, ...], None 代表正无穷
        """
        # 输入
        self._c = np.array(c) * 1.0
        self._A = np.array(A) * 1.0
        self._b = np.array(b) * 1.0
        self._lb = lb
        self._ub = ub
        # 输出
        self._sol = None  # solution
        self._obj_val = None  # objective value
        # 辅助变量
        self._iter_num = 0
        self._obj = None
        self._c1 = None
        self._A1 = None
        self._b1 = None
        self._model = None
        self._x1 = []
        self._sol1 = None
        self._const1 = []
        self._basic_consts = None  # tight constraints
        self._basic_vars = None
        self._non_basic_vars = None
        self._basic_matrix = None
        self._non_basic_matrix = None

    def _init_lb_ub(self):
        """ 初始化上下界
        """
        n = len(self._c)
        if self._lb is None:
            self._lb = [None] * n
        if self._ub is None:
            self._ub = [None] * n

    def _init_model(self):
        """ 根据输入，初始化模型。
        """
        self._model = pywraplp.Solver.CreateSolver('GLOP')
        # 约束：Ax <= b
        m, n = np.shape(self._A)
        self._x1 = [self._model.NumVar(0, self._model.Infinity(),
                                       'x[%d]' % j) for j in range(n)]
        for i in range(m):
            self._add_cut(self._x1, self._A[i, :], self._b[i])
        # 约束：lb <= x <= ub
        self._init_lb_ub()
        for j in range(n):
            # x <= ub
            if self._ub[j] is not None:
                self._add_cut([self._x1[j]], [1], self._ub[j])
            # -x <= -lb
            if self._lb[j] is not None:
                self._add_cut([self._x1[j]], [-1], -self._lb[j])
        # 目标
        self._obj = self._model.Objective()
        self._c1 = self._c
        for j in range(n):
            self._obj.SetCoefficient(self._x1[j], self._c1[j])
        self._obj.SetMaximization()

    def _add_cut(self, variables, coefficients, ub):
        """ 增加一个割平面
        """
        # 把不等式约束写成等式约束
        # ax <= ub --> ax + y = ub
        ct = self._model.Constraint(ub, ub)
        for x, c in zip(variables, coefficients):
            ct.SetCoefficient(x, c)
        # add slack variable
        slack_var = self._model.NumVar(0, self._model.Infinity(),
                                       'x[%d]' % len(self._x1))
        ct.SetCoefficient(slack_var, 1)
        self._x1.append(slack_var)
        self._const1.append(ct)

    def _refactor_cab(self):
        """ 把问题用标准形表示。
            min c1 * x1
            s.t. A1 * x1 = b1
        """
        m, n = len(self._const1), len(self._x1)
        self._c1 = np.array(self._c.tolist() + [0] * (n - len(self._c1)))
        self._A1 = np.zeros((m, n))
        self._b1 = np.zeros(m)
        for i in range(m):
            for j in range(n):
                self._A1[i][j] = self._const1[i].GetCoefficient(self._x1[j])
            self._b1[i] = self._const1[i].Ub()

    def _add_cuts_batch(self):
        """ 计算并添加割平面。
        """
        B_inv = np.linalg.inv(self._basic_matrix)
        N_bar = B_inv @ self._non_basic_matrix
        b1 = [self._b1[i] for i in self._basic_consts]
        b_bar = B_inv @ b1
        # generate cuts
        variables = [self._x1[j] for j in self._non_basic_vars]
        coefficients_batch = np.array([-N_bar[:, j] + np.floor(N_bar[:, j])
                                       for j in range(len(self._non_basic_vars))]).T
        ub_batch = -b_bar + np.floor(b_bar)
        # add all cuts
        for coefficients, ub in zip(coefficients_batch, ub_batch):
            self._add_cut(variables, coefficients, ub)

    def _solve_lp(self):
        """ 求解松弛问题。
        """
        self._model.Solve()
        # 把问题转换成标准化形式
        self._refactor_cab()
        # 然后计算辅助变量
        # 为下一步计算割平面做准备
        m, n = np.shape(self._A1)
        self._sol1 = [self._x1[j].solution_value() for j in range(n)]
        self._sol = self._sol1[0: len(self._c)]  # 原问题的解
        self._obj_val = self._obj.Value()  # 目标函数值
        self._basic_vars = [j for j in range(n)
                            if self._x1[j].basis_status() == self._model.BASIC]
        self._non_basic_vars = list(set(range(n)) - set(self._basic_vars))
        self._basic_consts = np.array([j for j in range(m)
                                       if self._const1[j].basis_status() == self._model.FIXED_VALUE])
        self._basic_matrix = np.array([[self._A1[i][j]
                                       for j in self._basic_vars]
                                       for i in self._basic_consts])
        self._non_basic_matrix = np.array([[self._A1[i][j]
                                           for j in self._non_basic_vars]
                                           for i in self._basic_consts])

    def _is_feasible(self):
        for v in self._sol1:
            if abs(v - np.round(v)) > 1e-6:
                return False
        return True

    def solve(self):
        self._init_model()  # 初始化松弛问题
        self._solve_lp()  # 求解松弛问题
        print("iter {}: obj = {}, x = {}"
              .format(self._iter_num, np.round(self._obj_val, 4), np.round(self._sol, 4)))
        while not self._is_feasible():
            self._add_cuts_batch()  # 添加割平面
            self._solve_lp()
            self._iter_num += 1
            print("iter {}: obj = {}, x = {}"
                  .format(self._iter_num, np.round(self._obj_val, 4), np.round(self._sol, 4)))


if __name__ == '__main__':
    from instances import instances
    ins = instances[3]
    CutPlane(ins['c'], ins['A'], ins['b'], ins['lb'], ins['ub']).solve()
