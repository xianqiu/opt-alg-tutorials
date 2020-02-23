import numpy as np

from master_model import MasterModel
from sub_model import SubModel


class CGProc(object):
    """
    Column Generation Process
    """
    def __init__(self, s, d, L, max_iter=10000):
        self._s = s  # 每种成品材料的长度
        for val in s:
            if val > L:
                raise ValueError("final size cannot be larger than raw size!")
        self._d = d  # 每种成品材料的需求
        self._L = L  # 原材料的长度
        self._reduced_cost = -1
        self._iter_times = 0
        self._max_iter = max_iter  # 最大的迭代次数
        self._status = -1  # -1:执行错误; 0:最优解; 1: 达到最大循环次数
        self._A = None  # Master problem对应的系数矩阵
        self._obj = None  # 目标值
        self._x = None  # Master problem对应的solution value
        self._solution_x = None  # 切割方式j需要的原材料数量
        self._solution_matrix = None  # 切割方式j

    def _stop_criteria_is_satisfied(self):
        if self._reduced_cost > -1e-6:
            self._status = 0
            return True
        if self._iter_times >= self._max_iter:
            if self._status == -1:
                self._status = 1
            return True
        return False

    def _init_basic_matrix(self):
        # 生成单位矩阵
        self._A = np.identity(len(self._s))

    def add_column(self, y):
        a = np.array(self._A)
        c = np.array(y).transpose()
        self._A = np.c_[a, c]

    def run(self):
        print("==== iter %d ====" % self._iter_times)
        self._init_basic_matrix()
        mp = MasterModel(self._A, self._d)
        mp.solve()
        mp.print_info()
        self._iter_times += 1
        while not self._stop_criteria_is_satisfied():
            # 1. 解Sub problem
            print("==== iter %d ====" % self._iter_times)
            sm = SubModel(mp.get_la(), self._s, self._L)
            sm.solve()

            # 2. 把生成的列加入到Master problem
            self.add_column(sm.get_solution())

            # 3. 解Master problem
            mp = MasterModel(self._A, self._d)
            mp.solve()
            self._x = mp.get_solution()
            self._obj = mp.get_objective_value()
            mp.print_info()

            # 4. 更新 reduced cost
            self._reduced_cost = 1 - sm.get_objective_value()
            sm.print_info()
            self._iter_times += 1

        self._get_solution()
        status_str = {-1: "error", 0: "optimal", 1: "attain max iteration"}
        print(">>> Terminated. Status:", status_str[self._status])

    def _get_solution_indices(self):
        # 计算有效的indices
        return [i for i in range(len(self._x)) if self._x[i] > 0]

    def _get_solution(self):
        """ 剔除冗余的结果
        """
        indices = self._get_solution_indices()
        self._solution_x = [self._x[i] for i in indices]
        self._solution_matrix = np.array([self._A[:, i] for i in indices]).transpose()

    def print_info(self):
        print("==== Column Generation Model Summary ====")
        print(" - Objective: Total number of raws needed =", self._obj)
        print(" - Fractional solution: The number of raws needed for each cutting pattern\n", self._solution_x)
        print(" - Solution matrix: Cutting patterns\n", self._solution_matrix)

    def get_solution_x(self):
        return self._solution_x

    def get_solution_matrix(self):
        return self._solution_matrix

