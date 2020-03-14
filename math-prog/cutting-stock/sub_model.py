from ortools.linear_solver import pywraplp


class SubModel(object):

    def __init__(self, sp, s, L):
        """
        :param sp: 主问题的shadow price(m维度向量), m代表成品材料的类型总数
        :param s: 成品材料的长度(m维向量)
        :param L: 原材料的总长度
        """
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self._sp = sp
        self._s = s
        self._L = L
        self._m = len(s)
        self._y = None  # 决策变量
        self._solution_y = None  # 计算结果

    def _init_decision_variables(self):
        self._y = [self._solver.IntVar(0, self._solver.Infinity(), "y[%d]" % i)
                   for i in range(self._m)]

    def _init_constraints(self):
        ct = self._solver.Constraint(0, self._L)
        for i in range(self._m):
            ct.SetCoefficient(self._y[i], self._s[i])

    def _init_objective(self):
        obj = self._solver.Objective()
        for i in range(self._m):
            obj.SetCoefficient(self._y[i], self._sp[i])
        obj.SetMaximization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        self._solution_y = [self._y[i].solution_value() for i in range(self._m)]

    def print_info(self):
        print("[Sub problem info]")
        print(" - Reduced cost of master problem =", 1 - self.get_objective_value())
        print(" - New column generated:", self._solution_y)

    def get_solution(self):
        return self._solution_y

    def get_objective_value(self):
        return sum(map(lambda x: x[0]*x[1], zip(self._sp, self._solution_y)))
