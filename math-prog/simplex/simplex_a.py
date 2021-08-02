import numpy as np


class SimplexA(object):
    """
    单纯形算法（基本版）。
    Note:
        1、系数矩阵满秩。
        2、未处理退化情形。
        3、输入基本可行解（对应的列）。
    """
    def __init__(self, c, A, b, v0):
        """
        :param c: n * 1 vector
        :param A: m * n matrix
        :param b: m * 1 vector
        :param v0: basic variables, list of variable indices
        注意：v0是 B 的列下标。x0 = B^{-1}b 即为基本可行解（需要保证x0非负）。
        """
        # 输入
        self._c = np.array(c)
        self._A = np.array(A)
        self._b = np.array(b)
        self._basic_vars = v0
        self._non_basic_vars = self._init_non_basic_vars()
        self._m = len(A)
        self._n = len(c)
        # 辅助变量
        self._iter_num = 0
        self._B_inv = None  # inverse of B
        self._lambda_t = None  # shadow price
        self._mu_t = None  # reduced cost
        # 输出
        self._obj = None  # objective function value
        self._sol = None  # solution
        self._status = None

    def _init_non_basic_vars(self):
        # initialize nonbasic variables
        non_basic_vars = []
        for j in range(self._n):
            if j not in self._basic_vars:
                non_basic_vars.append(j)
        return non_basic_vars

    def _update_reduced_cost(self):
        B = np.array([self._A[:, j] for j in self._basic_vars]).transpose()
        self._B_inv = np.linalg.inv(B)
        # transpose of c_B
        c_B_t = np.array([self._c[j] for j in self._basic_vars])
        # shadow price
        self._lambda_t = np.dot(c_B_t, self._B_inv)
        N = np.array([self._A[:, j] for j in self._non_basic_vars]).transpose()
        c_N_t = np.array([self._c[j] for j in self._non_basic_vars])
        # reduced cost
        self._mu_t = np.dot(self._lambda_t, N) - c_N_t

    def _is_optimal(self):
        if max(self._mu_t) > 1e-6:
            return False
        return True

    def _pivot(self):
        """ 选主元，入基和出基。
        """
        j_ind = np.argmax(self._mu_t)
        # 入基变量 x_j
        j = self._non_basic_vars[j_ind]
        # 出基变量 x_i
        i = self._minimum_ratio_test(j)
        if i is None:
            self._status = 'UNBOUNDED'
            return
        # update basic vars
        for k in range(self._m):
            if self._basic_vars[k] == i:
                self._basic_vars[k] = j
                break
        # update non basic vars
        self._non_basic_vars[j_ind] = i

    def _minimum_ratio_test(self, j):
        """ Minimum Ratio Test.
        给定入基的非基变量，返回出基的基变量。
        :param j: 入基变量 x_j 的下标 j
        :return: 出基变量 x_i 的下标 i
        """
        b_bar = np.dot(self._B_inv, self._b)
        a_in = np.dot(self._B_inv, self._A[:, j])
        ratios = list(map(lambda b, a: b/a if a > 1e-6 else np.infty, b_bar, a_in))
        i_ind = np.argmin(ratios)
        if ratios[i_ind] != np.infty:
            return self._basic_vars[i_ind]
        else:
            return None

    def _update_obj(self):
        self._obj = np.dot(self._lambda_t, self._b)

    def _update_solution(self):
        x_B = np.dot(self._B_inv, self._b)
        self._sol = [0] * self._n
        for k in range(self._m):
            self._sol[self._basic_vars[k]] = x_B[k]

    def _print_iter_info(self, is_print):
        if not is_print:
            return
        print("==== iteration {} ====".format(self._iter_num))
        print("+ basic variables: {}".format(self._basic_vars))
        print("+ shadow price: {}".format(self._lambda_t))
        print("+ reduced cost: {}".format(self._mu_t))
        print("+ objective = {}".format(self._obj))
        print("+ x = {}".format(self._sol))

    def solve(self, print_info=True):
        self._iter_num = 0
        self._update_reduced_cost()
        self._update_obj()
        self._update_solution()
        self._print_iter_info(print_info)
        while not self._is_optimal():
            if self._status == "UNBOUNDED":
                break
            self._pivot()
            self._update_reduced_cost()
            self._update_obj()
            self._update_solution()
            self._iter_num += 1
            self._print_iter_info(print_info)
        if self._status != "UNBOUNDED":
            self._status = 'OPTIMAL'
        if print_info:
            print("Done >> status: {}".format(self._status))

        return self

    def get_basic_vars(self):
        return self._basic_vars

    def get_objective(self):
        return self._obj

    def get_solution(self):
        return self._sol

    def get_status(self):
        return self._status


if __name__ == '__main__':
    from instances import instances
    ins = instances[0]  # Normal
    SimplexA(ins['c'], ins['A'], ins['b'], ins['v0']).solve()
    ins = instances[2]  # Unbounded
    SimplexA(ins['c'], ins['A'], ins['b'], ins['v0']).solve()

