import numpy as np


class DualSimplex(object):
    """
        对偶单纯形算法（基本版）。
        Note:
            1、系数矩阵满秩。
            2、未处理退化情形。
            3、输入对偶可行解（对应的列）。
    """

    def __init__(self, c, A, b, v1):
        """
        :param c: n * 1 vector
        :param A: m * n matrix
        :param b: m * 1 vector
        :param v1: dual feasible solution, list of column indices
        """
        # 输入
        self._c = np.array(c)
        self._A = np.array(A)
        self._b = np.array(b)
        self._basic_vars = v1
        self._m = len(A)
        self._n = len(c)
        self._non_basic_vars = self._init_non_basic_vars()
        # 辅助变量
        self._iter_num = 0
        self._B_inv = None
        self._N_bar = None  # N_bar = B^{-1}N
        self._y = None  # dual solution (i.e., shadow price)
        # 输出
        self._sol = None  # primal solution
        self._obj_dual = None  # dual objective
        self._status = None

    def _init_non_basic_vars(self):
        # initialize nonbasic variables
        non_basic_vars = []
        for j in range(self._n):
            if j not in self._basic_vars:
                non_basic_vars.append(j)
        return non_basic_vars

    def _is_optimal(self):
        """ x >= 0 implies optimality.
        """
        for x in self._sol:
            if x < 0:
                return False
        return True

    def _update_solutions(self):
        B = np.array([self._A[:, j] for j in self._basic_vars]).transpose()
        self._B_inv = np.linalg.inv(B)
        # primal solution (infeasible)
        self._sol = [0] * self._n
        x_B = self._B_inv @ self._b
        for k in range(self._m):
            self._sol[self._basic_vars[k]] = x_B[k]
        # dual feasible solution
        c_B = np.array([self._c[j] for j in self._basic_vars])
        self._y = self._B_inv.T @ c_B

    def _update_obj(self):
        self._obj_dual = self._b @ self._y

    def _pivot(self):
        # 出基变量 x_i
        i = int(np.argmin(self._sol))
        # 出基变量 x_i 在 self._basic_vars 中的index
        i_ind = None
        for k in range(self._m):
            if self._basic_vars[k] == i:
                i_ind = k
                break
        # 判断原问题是否可行
        # 对偶问题无界，则原问题不可行
        if not self._check_feasibility(i_ind):
            self._status = 'INFEASIBLE'
            return
        # 入基变量 x_j 在 self._basic_vars 中的index
        j_ind = self._minimum_ratio_test(i_ind)
        # 入基变量 x_j
        j = self._non_basic_vars[j_ind]
        # update basic vars
        for k in range(self._m):
            if self._basic_vars[k] == i:
                self._basic_vars[k] = j
                break
        # update non basic vars
        self._non_basic_vars[j_ind] = i

    def _check_feasibility(self, row_ind):
        N = np.array([self._A[:, j] for j in self._non_basic_vars]).transpose()
        self._N_bar = self._B_inv @ N
        for x in self._N_bar[row_ind]:
            if x < 0:
                return True
        return False

    def _minimum_ratio_test(self, ind_out):
        N = np.array([self._A[:, j] for j in self._non_basic_vars]).transpose()
        c_N = np.array([self._c[j] for j in self._non_basic_vars])
        c_bar = c_N - self._y @ N
        self._N_bar = self._B_inv @ N
        a_bar = self._N_bar[ind_out] * -1
        ratios = list(map(lambda c, a: c/a if a > 0 else np.infty, c_bar, a_bar))
        return int(np.argmin(ratios))

    def _print_info(self):
        print("==== iteration {} ====".format(self._iter_num))
        print("+ basic variables: {}".format(self._basic_vars))
        print("+ dual objective: {}".format(self._obj_dual))
        print("+ x = {}".format(self._sol))

    def _check_init_solution(self):
        """ Check feasibility of the initial dual solution.
        """
        B = np.array([self._A[:, j] for j in self._basic_vars]).transpose()
        self._B_inv = np.linalg.inv(B)
        N = np.array([self._A[:, j] for j in self._non_basic_vars]).transpose()
        self._N_bar = self._B_inv @ N
        c_B = np.array([self._c[j] for j in self._basic_vars])
        c_N = np.array([self._c[j] for j in self._non_basic_vars])
        self._y = c_B @ self._B_inv
        mu = c_N - self._y @ N
        for x in mu:
            if x < 0:
                raise ValueError('Initial solution is not dual feasible!')

    def solve(self):
        self._iter_num = 0  # 记录迭代次数
        self._check_init_solution()  # 检查初始的对偶解是否可行
        self._update_solutions()
        self._update_obj()
        self._print_info()
        while not self._is_optimal():  # 判断是否最优或者不可行
            if self._status == "INFEASIBLE":
                break
            self._pivot()  # 迭代（选主元入基，执行Minimum Ratio Test，然后出基）
            self._update_solutions()
            self._update_obj()
            self._iter_num += 1
            self._print_info()

        if self._status != 'INFEASIBLE':
            self._status = 'OPTIMAL'
        print("Done >> status: {}".format(self._status))


if __name__ == '__main__':
    from instances import instances
    ins = instances[0]  # normal
    DualSimplex(ins['c'], ins['A'], ins['b'], ins['v1']).solve()
    ins = instances[1]  # normal
    DualSimplex(ins['c'], ins['A'], ins['b'], ins['v1']).solve()
    ins = instances[4]  # primal degenerate
    DualSimplex(ins['c'], ins['A'], ins['b'], ins['v1']).solve()
    ins = instances[5]  # primal degenerate
    DualSimplex(ins['c'], ins['A'], ins['b'], ins['v1']).solve()
    ins = instances[12]  # infeasible
    DualSimplex(ins['c'], ins['A'], ins['b'], ins['v1']).solve()
