from master_model import MasterModel
from sub_model import SubModel


class DWProc(object):

    def __init__(self, p, c, d, b, max_iter=1000):
        """
        :param p: p[i][j]代表品牌i中商品j的预期收益
        :param c: c[i][j]代表品牌i中商品j的营销成本
        :param d: 总营销成本, int
        :param b: b[i]代表选中品牌i的商品数量限制
        """
        self._p = p
        self._c = c
        self._d = d
        self._b = b
        self._v = None  # 待初始化
        self._max_iter = max_iter
        self._iter_times = 0
        self._status = -1
        self._reduced_costs = [1] * len(self._p)
        self._solution_x = None  # 计算结果
        self._obj_value = 0  # 目标函数值

    def _stop_criteria_is_satisfied(self):
        """ 根据reduced cost判断是否应该停止迭代.
        注意: 这是最大化问题, 因此所有子问题对应的reduced cost <= 0时停止.
        """
        st = [0] * len(self._reduced_costs)
        for i in range(len(self._reduced_costs)):
            if self._reduced_costs[i] < 1e-6:
                st[i] = 1
        if sum(st) == len(st):
            self._status = 0
            return True
        if self._iter_times >= self._max_iter:
            if self._status == -1:
                self._status = 1
            return True
        return False

    def _init_v(self):
        """ 初始化主问题的输入
        """
        self._v = [[]] * len(self._p)
        for i in range(len(self._p)):
            self._v[i] = [[0] * len(self._p[i])]

    def _append_v(self, i, x):
        """ 把子问题i的解加入到主问题中

        :param x: 子问题i的解
        """
        self._v[i].append(x)

    def solve(self):
        # 初始化主问题并求解
        self._init_v()
        mp = MasterModel(self._p, self._v, self._c, self._d)
        mp.solve()
        self._iter_times += 1
        # 迭代求解主问题和子问题直到满足停止条件
        while not self._stop_criteria_is_satisfied():
            # 求解子问题
            print("==== iter %d ====" % self._iter_times)
            for i in range(len(self._p)):
                # 求解子问题
                sm = SubModel(self._p[i], self._c[i], mp.get_y(), self._b[i])
                sm.solve()
                # 更新reduced cost
                self._reduced_costs[i] = sm.get_obj_value() - mp.get_zi(i)
                # 把子问题中满足条件的解加入到主问题中
                if self._reduced_costs[i] > 0:
                    self._append_v(i, sm.get_solution_x())
                print(">>> Solve sub problem %d, reduced cost = %f" % (i, self._reduced_costs[i]))

            # 求解主问题
            mp = MasterModel(self._p, self._v, self._c, self._d)
            mp.solve()

            self._iter_times += 1

        self._solution_x = mp.get_solution_x()
        self._obj_value = mp.get_obj_value()
        status_str = {-1: "error", 0: "optimal", 1: "attain max iteration"}
        print(">>> Terminated. Status:", status_str[self._status])

    def print_info(self):
        print("==== Result Info  ====")
        print(">>> objective value =", self._obj_value)
        print(">>> Solution")
        sku_list = [[]] * len(self._solution_x)
        for i in range(len(self._solution_x)):
            sku_list[i] = [j for j in range(len(self._solution_x[i])) if self._solution_x[i][j] > 0]
        for i in range(len(self._solution_x)):
            print("brand %d, sku list:" % i, sku_list[i])
