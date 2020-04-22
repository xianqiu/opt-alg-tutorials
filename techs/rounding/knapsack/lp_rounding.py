from ortools.linear_solver import pywraplp



class KnapsackLPRounding(object):
    """ 背包问题LP Rounding(近似)解法.
    """

    def __init__(self, w, p, W):
        """
        :param w: 物品大小, list
        :param p: 物品价值, list
        :param W: 背包大小, int
        """
        self._w = w
        self._p = p
        self._W = W
        self._n = len(self._w)
        self._result = None

    def _solve_lp(self):
        solver = pywraplp.Solver('MasterModel', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        n = len(self._w)
        # 决策变量
        x = [solver.NumVar(0, 1, 'x[%d]' % i) for i in range(n)]
        # 约束
        ct = solver.Constraint(0, self._W)
        for i in range(n):
            ct.SetCoefficient(x[i], self._w[i])
        # 目标
        obj = solver.Objective()
        for i in range(n):
            obj.SetCoefficient(x[i], self._p[i])
        obj.SetMaximization()
        # 求解
        solver.Solve()
        # 得到计算结果
        return [x[i].solution_value() for i in range(n)]

    def _rounding(self, x):
        """ 对分数解x取整, 然后从剩余商品中挑一个价值最大的商品装入背包(如果可行）
        """
        sol = [i for i in range(len(x)) if abs(x[i] - 1) < 1e-6]
        # 背包剩余的空间
        available_space = self._W - sum([self._w[i] for i in sol])
        # 剩下的物品
        left_over = set(range(self._n)) - set(sol)
        # 剩下物品的价值
        left_over_profits = [self._p[i] for i in left_over]
        # 按从大到小排序
        left_over_items = list(sorted(zip(left_over, left_over_profits), key=lambda item: item[1], reverse=True))
        left_over = [item[0] for item in left_over_items if self._w[item[0]] <= available_space]

        return sol + [left_over[0]] if left_over else sol

    def solve(self):
        # 求解背包问题的松弛解
        x = self._solve_lp()
        # Rounding solution
        self._result = self._rounding(x)
        return self

    def print_result(self):
        print("Packed items:", self._result)
        print("Total profit:", sum([self._p[i] for i in self._result]))
        print("Total weight:", sum([self._w[i] for i in self._result]))


if __name__ == '__main__':

    W = 67
    p = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    w = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]

    knapsack = KnapsackLPRounding(w, p, W).solve()
    knapsack.print_result()




