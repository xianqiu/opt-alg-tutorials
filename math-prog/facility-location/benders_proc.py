import numpy as np

from master_model import MasterModel
from sub_model import SubModel


class BendersProc(object):
    """ Benders分解流程
    """

    def __init__(self, f, C, max_iter=10000):
        """
        :param f: 开仓成本(m维向量)
        :param C: 连接成本(m*n矩阵), 其中m是候选设施的数量, n是客户的数量
        :param max_iter: 最大循环次数
        """
        self._f = f
        self._c = C
        self._iter_times = 0
        self._max_iter = max_iter
        self._status = -1  # -1:执行错误; 0:最优解; 1: 达到最大循环次数
        self._ub = np.inf
        self._lb = -np.inf
        self._solution_x = None  # 计算结果
        self._solution_y = None  # 计算结果

    def _stop_criteria_is_satisfied(self):
        """ 根据上下界判断是否停止迭代
        """
        if self._ub - self._lb < 0.0001:
            self._status = 0
            return True
        if self._iter_times >= self._max_iter:
            if self._status == -1:
                self._status = 1
            return True
        return False

    def solve(self):
        # 初始令z=0. 求解主问题得到y
        master0 = MasterModel(self._f, fix_z=0)
        master0.solve()
        y, z = master0.get_solution()
        # 下面的迭代需要重新生成master对象
        # 因为master0中z=0是约束条件
        master = MasterModel(self._f)
        sub = None
        # 迭代过程
        while not self._stop_criteria_is_satisfied():
            # 求解子问题
            sub = SubModel(y, self._c)
            sub.solve()
            # 更新上界
            fy = sum(np.array(self._f) * np.array(y))
            self._ub = min(self._ub, fy + sub.get_objective_value())
            # 生成主问题的约束
            alpha, beta = sub.get_solution()
            master.add_constraint(alpha, beta)
            master.solve()
            # 更新y和下界
            y, z = master.get_solution()
            self._lb = master.get_objective_value()

            print(">>> iter %d: lb = %.4f, ub = %.4f" % (self._iter_times, self._lb, self._ub))
            self._iter_times += 1

        # 保存结果
        self._solution_x = sub.get_dual_values()
        self._solution_y = y

        status_str = {-1: "error", 0: "optimal", 1: "attain max iteration"}
        print(">>> Terminated. Status:", status_str[self._status])

    def print_info(self):
        print("---- Solution ----")
        res = {}
        for i in range(len(self._f)):
            if self._solution_y[i] == 0:
                continue
            connected_cities = [str(j) for j in range(len(self._c[0]))
                                if self._solution_x[i][j] > 0]
            res[i] = ', '.join(connected_cities)

        for f, c in res.items():
            print("open facility: %d, connected cities: %s" % (f, c))







