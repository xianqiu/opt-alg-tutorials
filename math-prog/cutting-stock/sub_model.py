from ortools.linear_solver import pywraplp


class SubModel(object):

    def __init__(self, la, s, L):
        self._solver = pywraplp.Solver('MasterModel',
                                       pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self._la = la
        self._s = s
        self._L = L
        self._m = len(s)
        self._y = None  # 决策变量
        self._solution_y = None
        self._obj = None

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
            obj.SetCoefficient(self._y[i], self._la[i])
        obj.SetMaximization()

    def solve(self):
        self._init_decision_variables()
        self._init_constraints()
        self._init_objective()
        self._solver.Solve()
        self._solution_y = [self._y[i].solution_value() for i in range(self._m)]
        self._obj = sum(map(lambda x: x[0]*x[1], zip(self._la, self._solution_y)))

    def print_info(self):
        print("[Sub problem info]")
        print(" - Reduced cost of master problem =", 1 - self._obj)
        print(" - New column generated:", self._solution_y)

    def get_solution(self):
        return self._solution_y

    def get_objective_value(self):
        return self._obj
