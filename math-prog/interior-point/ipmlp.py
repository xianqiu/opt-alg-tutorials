import numpy as np


class IPMlp(object):

    """ A Primal Dual Interior Point Method for linear programming.
    说明：
    1. 最小化问题
    2. 行满秩
    """

    def __init__(self, c, A, b):
        """
        :param c: n * 1 vector
        :param A: m * n matrix
        :param b: m * 1 vector
        """
        # 输入
        self._c = np.array(c)
        self._A = np.array(A)
        self._b = np.array(b)

        # 输出
        self._obj = None  # objective function value
        self._x = None  # primal solution
        self._y = None  # dual solution

        # 辅助变量
        self._m = len(self._b)
        self._n = len(self._c)
        self._s = None  # dual slack variable
        self._alpha = None
        self._sigma = None
        self._mu = None
        self._iter_num = 0
        self._status = None

    def _init(self):
        """ 初始化
        满足条件：x > 0，s > 0 即可。
        """
        self._x = np.ones(self._n)
        self._s = np.ones(self._n)
        self._y = np.ones(self._m)
        self._alpha = 1
        self._sigma = 0.1
        self._mu = self._x @ self._s / self._n
        self._epsilon = 1e-6  # optimality tolerance

    def _solve_linear_system(self):
        A = np.block([[self._A, np.zeros((self._m, self._m)), np.zeros((self._m, self._n))],
                      [np.zeros((self._n, self._n)), self._A.T, np.eye(self._n)],
                      [np.eye(self._n) * self._s, np.zeros((self._n, self._m)), np.eye(self._n) * self._x]])

        if np.linalg.matrix_rank(A) < 2 * self._n + self._m:
            return None, None, None

        b0 = self._A @ self._x - self._b
        b1 = self._A.T @ self._y + self._s - self._c
        b2 = self._x * self._s * np.eye(self._n) @ np.ones(self._n) \
            - self._mu * np.ones(self._n)

        b = np.array(b0.tolist() + b1.tolist() + b2.tolist())
        sol = np.linalg.solve(A, -b)
        dx = sol[0: self._n]
        dy = sol[self._n: self._n + self._m]
        ds = sol[self._n + self._m:]

        return dx, dy, ds

    def _get_alpha(self, dx, ds):
        ratios = [-self._x[i] / dx[i] for i in range(self._n) if dx[i] < 0]
        ratios += [-self._s[i] / ds[i] for i in range(self._n) if ds[i] < 0]
        alpha = min(ratios) if len(ratios) else 1

        return min(1, alpha * 0.99)

    def _print_iter_info(self):
        print("==== iteration {} ====".format(self._iter_num))
        print("+ mu = {}, alpha = {}".format(self._mu, self._alpha))
        print("+ x = {}".format(self._x))
        print("+ y = {}".format(self._y))
        print("+ s = {}".format(self._s))
        print("+ objective = {}".format(self._obj))

    def _is_stop_criterion_satisfied(self):
        ex = self._A @ self._x - self._b
        ey = self._A.T @ self._y + self._s - self._c
        duality_gap = self._x @ self._s
        err = max(ex @ ex, ey @ ey, duality_gap)
        if err < self._epsilon:
            return True
        return False

    def solve(self):
        self._init()  # initialization
        while not self._is_stop_criterion_satisfied():
            # solve Newton system
            dx, dy, ds = self._solve_linear_system()
            if dx is None:
                self._status = 'UNBOUNDED or INFEASIBLE'
                break
            # determine step size
            self._alpha = self._get_alpha(dx, ds)
            # update values
            self._x += self._alpha * dx
            self._y += self._alpha * dy
            self._s += self._alpha * ds
            # shrink mu
            self._mu = (self._x @ self._s / self._n) * self._sigma
            self._obj = self._c @ self._x

            self._iter_num += 1
            self._print_iter_info()

        if self._status is None:
            self._status = 'OPTIMAL'

        print("Done >> status: {}".format(self._status))

        return self


if __name__ == '__main__':

    ins = {
        'c': [-3, -4, -2, 0, 0, 0],
        'A': [[2, 0, 0, 1, 0, 0],
              [1, 0, 2, 0, 1, 0],
              [0, 3, 1, 0, 0, 1]],
        'b': [4, 8, 6],
        'opt': -16
    }

    ipm = IPMlp(ins['c'], ins['A'], ins['b'])
    ipm.solve()
