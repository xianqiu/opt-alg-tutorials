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
    """

    def _minimum_ratio_test(self, var_in):
        """ Lexicographically minimum ratio test.
        """
        a_in = np.dot(self._B_inv, self._A[:, var_in])
        d0 = self._get_initial_out_candidates(a_in)
        if d0 is None:
            return None
        # The index of "basic_vars".
        # The associated basic variable will be moved out.
        out_index = self._get_out_ind(d0, 0, a_in)
        return self._basic_vars[out_index]

    def _get_initial_out_candidates(self, a_in):
        b_bar = np.dot(self._B_inv, self._b)
        ratios = list(map(lambda b, a: b / a if a > 1e-6 else np.infty, b_bar, a_in))
        d0 = arg_min(ratios)
        if ratios[d0[0]] == np.infty:
            return None
        return d0

    def _get_out_ind(self, out_candidates, j, a_in):
        """
        :param out_candidates:
        :param j: the jth iteration (j=0 at the beginning).
        :param a_in: column A[:, var_in]
        :return: the index to "basic_vars" (to be moved out)
        """
        if len(out_candidates) == 1:
            return out_candidates[0]
        aj = np.dot(self._B_inv, self._A[:, j])
        ratios = []
        for k in out_candidates:
            ratios.append(aj[k] / a_in[k])
        indices = arg_min(ratios)
        out_int_set1 = [out_candidates[k] for k in indices]
        return self._get_out_ind(out_int_set1, j + 1, a_in)
