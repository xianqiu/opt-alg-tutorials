import numpy as np
from copy import deepcopy


class RoundingProc(object):

    def __init__(self, A, x, s, d, L):
        """
        :param A: 可行切割矩阵(每列代表一种切割方式)(m*n维矩阵),
                  其中m代表成品材料类型总数, n是我们考虑的可行切割方式的数量
        :param x: 切割方式需要的原材料数量(fractional)(n维向量)
        :param s: 成品材料的尺寸(m维向量)
        :param d: 成品材料的尺寸对应的需求量(m维向量)
        :param L: 原材料的长度
        """
        self._A = np.array(A)
        self._x = x
        self._s = s
        self._d = d
        self._L = L
        self._d0 = None  # 被满足的需求量
        self._d1 = None  # 未被满足的需求量
        self._greedy_x = None  # 贪心算法的结果: 对应满足d1的部分
        self._greedy_matrix = None  # 贪心算法的结果: 对应满足d1的部分
        self._solution_x = None  # 最终结果: 切割方式对应的数量
        self._solution_matrix = None  # 最终结果: 切割方式对应的矩阵

    def _round_down(self):
        """ 把分数解self._x向下取整, 然后计算未被满足的需求量.
        """
        self._x = list(map(int, self._x))

        # 计算被满足的需求量
        def cal_d0(i):
            return sum(self._A[i] * np.array(self._x))

        self._d0 = [cal_d0(i) for i in range(len(self._d))]

        # 计算未被满足的需求量
        self._d1 = (np.array(self._d) - np.array(self._d0)).tolist()

    def _satisfy(self):
        """ 用贪心的方式满足需求
        :return: 切割方式矩阵
        """
        # 把index按成品材料的长度从大到小排序
        sorted_indices = list(np.argsort(-np.array(self._s)))
        rows = []
        x = []
        d1 = deepcopy(self._d1)
        while sum(d1) > 0:
            c = self._greedy_cut(d1, sorted_indices)
            if not rows:
                rows.append(c)
                x.append(1)
            else:
                if rows[-1] != c:
                    rows.append(c)
                    x.append(1)
                else:
                    x[-1] += 1
            # 更新需求
            d1 = (np.array(d1) - np.array(c)).tolist()

        return x, np.array(rows).transpose()

    def _greedy_cut(self, d1, sorted_indices):
        """ 用贪心的方式切割1根原材料.
        :param d1: 未被满足的需求
        :param sorted_indices: 成品材料的长度从大到小排序对应的indices
        :return: 切割方式,m维向量(m=成品材料的个数)
        """
        c = [0] * len(self._d)
        raw_len = self._L
        for i in sorted_indices:
            c[i] = min(raw_len // self._s[i], d1[i])
            raw_len -= c[i] * self._s[i]
        return c

    def solve(self):
        self._round_down()
        self._greedy_x, self._greedy_matrix = self._satisfy()
        self._solution_x = self._x + self._greedy_x
        self._solution_matrix = np.c_[self._A, self._greedy_matrix]

    def print_info(self):
        print("==== Rounding Process Summary ====")
        print("[Round down result]")
        print(" - Integer solution\n", self._x)
        print(" - Unsatisfied demands\n", self._d1)
        print("[Greedy result]")
        print(" - solution (w.r.t. unsatisfied demand)\n", self._greedy_x)
        print(" - Solution matrix(w.r.t. unsatisfied demand)\n", self._greedy_matrix)
        print("[Final result]")
        print(" - Objective value: The total number of raws needed =", sum(self._solution_x))
        print(" - Solution: The number of raws needed for each cutting pattern \n", self._solution_x)
        print(" - Solution matrix: Cutting patterns\n", self._solution_matrix)
        d0 = [sum(self._solution_matrix[i] * np.array(self._solution_x)) for i in range(len(self._d))]
        print(" - Satisfied demands: \n", d0)

