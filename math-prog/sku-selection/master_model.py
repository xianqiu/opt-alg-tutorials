from ortools.linear_solver import pywraplp


class MasterModel(object):

    def __init__(self, p, v, c, d):
        """
        :param p: p[i][j]代表品牌i中商品j的预期收益
        :param v: v[i]代表第i个子问题的解
        :param c: c[i][j]代表品牌i中商品j的营销成本
        :param d: scalar, 总预算
        """
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        self._p = p
        self._v = v
        self._c = c
        self._d = d
        self._la = None  # 决策变量lambda
        self._constraint_y = None  # 约束
        self._constraint_z = []  # 约束
        self._solution_la = None  # 计算结果

    def _init_decision_variables(self):
        self._la = [[]] * len(self._v)
        self._solution_la = [[]] * len(self._v)  # 初始化保存结果的变量
        for i in range(len(self._v)):
            self._la[i] = [[]] * len(self._v[i])
            self._solution_la[i] = [[]] * len(self._v[i])  # 初始化保存结果的变量
            for k in range(len(self._v[i])):
                self._la[i][k] = self._solver.NumVar(0, 1, 'la[%d][%d]' % (i, k))

    def _init_constraints(self):
        self._constraint_y = self._solver.Constraint(0, self._d)
        for i in range(len(self._v)):
            for k in range(len(self._v[i])):
                f = 0
                for j in range(len(self._v[i][k])):
                    f += self._c[i][j] * self._v[i][k][j]
                self._constraint_y.SetCoefficient(self._la[i][k], f)

        self._constraint_z = [None] * len(self._v)
        for i in range(len(self._v)):
            self._constraint_z[i] = self._solver.Constraint(1, 1)
            for k in range(len(self._la[i])):
                self._constraint_z[i].SetCoefficient(self._la[i][k], 1)

    def _init_objective(self):
        obj = self._solver.Objective()
        for i in range(len(self._v)):
            for k in range(len(self._v[i])):
                f = 0
                for j in range(len(self._v[i][k])):
                    f += self._p[i][j] * self._v[i][k][j]
                obj.SetCoefficient(self._la[i][k], f)
        obj.SetMaximization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        # 保存计算结果
        for i in range(len(self._v)):
            for k in range(len(self._v[i])):
                self._solution_la[i][k] = self._la[i][k].solution_value()

    def get_solution_value(self):
        return self._solution_la

    def get_y(self):
        """ 获取对偶变量y的值
        """
        return self._constraint_y.dual_value()

    def get_zi(self, i):
        """ 获取对偶变量z[i]的值
        """
        return self._constraint_z[i].dual_value()

    def get_obj_value(self):
        res = 0
        for i in range(len(self._p)):
            for k in range(len(self._v[i])):
                for j in range(len(self._p[i])):
                    res += self._solution_la[i][k] * self._p[i][j] * self._v[i][k][j]
        return res

    def get_solution_x(self):
        """ 得到原问题的解.  x[i][j] = sum(la[i][k] * v[i][k][j]) over k.
        """

        x = [[]] * len(self._v)
        for i in range(len(self._v)):
            x[i] = [0] * len(self._v[i][0])

        for i in range(len(self._v)):
            for k in range(len(self._v[i])):
                for j in range(len(self._v[i][k])):
                    x[i][j] += self._solution_la[i][k] * self._v[i][k][j]
        return x

