from simplex_a import SimplexA
import numpy as np


def arg_min(arr):
    """ 给定数组，返回 ”所有“ 最小值的index。
    """
    v = np.infty
    res = []
    for i in range(len(arr)):
        if arr[i] == v:
            res.append(i)
        elif arr[i] < v:
            res = [i]
            v = arr[i]
    return res


class SimplexAD(SimplexA):
    """
    单纯形算法：处理退化情形。
    Note:
        1、系数矩阵满秩。
        3、输入基本可行解（对应的列）。
    """

    def _minimum_ratio_test(self, j):
        """ Lexicographically minimum ratio test.
        :param j: 入基变量 x_j 的下标 j
        :return: 出基变量 x_i 的下标 i
        """
        a_in = np.dot(self._B_inv, self._A[:, j])
        d0 = self._get_d0(a_in)  # 计算 I_0 的数组下标
        if d0 is None:
            return None
        # The index of "basic_vars".
        # The associated basic variable will be moved out.
        i_ind = self._get_out_ind(d0, 0, a_in)
        return self._basic_vars[i_ind]

    def _get_d0(self, a_in):
        """ 根据 Minimum Ratio Test 计算 I_0.
        实际上计算 d0 即可（定义如下）：
        1、计算 ratios = [r_1, r_2, ..., r_m].
        2、计算 d0 = arg min(ratios)，即 ratios 中最小值的下标
        3、I_0 = [self._basic_vars[i] for i in d0]
        """
        b_bar = np.dot(self._B_inv, self._b)
        ratios = list(map(lambda b, a: b / a if a > 1e-6 else np.infty, b_bar, a_in))
        d0 = arg_min(ratios)
        if ratios[d0[0]] == np.infty:
            # a_in 的分量 <= 0
            # 最优目标函数值无界
            return None
        return d0

    def _get_out_ind(self, d0, it, a_in):
        """ 用递归的方法计算出基变量（在self._basic_vars[]中的index）.
        :param d0: I_0 （在self._basic_vars[]的indices）.
        :param it: iteration number, equals 0 at the beginning.
        :param a_in: B_inv * A[:, j]
        :return: the index to "basic_vars" (to be moved out)
        """
        if len(d0) == 1:
            return d0[0]
        a_it = np.dot(self._B_inv, self._A[:, it])
        ratios = [a_it[k] / a_in[k] for k in d0]
        indices = arg_min(ratios)
        d1 = [d0[k] for k in indices]
        return self._get_out_ind(d1, it + 1, a_in)


if __name__ == '__main__':
    from instances import instances
    # ins = instances[4]  # degenerate
    # SimplexAD(ins['c'], ins['A'], ins['b'], ins['v0']).solve()
    ins = instances[11]  # degenerate
    SimplexAD(ins['c'], ins['A'], ins['b'], ins['v0']).solve()

