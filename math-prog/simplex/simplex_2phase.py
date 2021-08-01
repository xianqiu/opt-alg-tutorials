import numpy as np

from simplex_ad import SimplexAD


class Simplex2P(object):

    def __init__(self, c, A, b):
        self._c = c
        self._A = A
        self._b = b
        self._m = len(self._A)
        self._n = len(self._c)
        self._status = None
        # The following variables are for phase 1
        self._ins1 = self._construct_phase1_instance()
        self._basic_vars = []
        self._basic_art_vars = []
        self._basic_art_vars_num = 0
        # 处理退化情形的中间变量
        # R = B^{-1}*N.
        # R12 对应 R 的前 k 列，其中 k 代表 basic non artificial variable 的个数
        self._R12 = None

    def _construct_phase1_instance(self):
        c1 = [0] * self._n + [1] * self._m
        I = np.eye(self._m)
        A = self._A
        A1 = np.array(np.bmat("A I"))
        b1 = self._b
        v0 = [i + self._n for i in range(self._m)]
        return c1, A1, b1, v0

    def _initialize(self):
        # solve phase1 problem
        sim = SimplexAD(*self._ins1).solve(print_info=False)

        # check feasibility
        if abs(sim.get_objective()) > 1e-6 or sim.get_status() != 'OPTIMAL':
            self._status = 'INFEASIBLE'
            return

        # If feasible, consider the following two cases.
        # Case1(normal): artificial vars not in basic vars.
        self._basic_vars = sim.get_basic_vars()
        print("init basic vars =", self._basic_vars)

        # Case2(degenerate): artificial vars in basic vars.
        # Then exchange artificial columns with non-basic columns.
        self._basic_art_vars = [i for i in self._basic_vars if i >= self._n]
        self._basic_art_vars_num = len(self._basic_art_vars)
        if self._basic_art_vars_num > 0:
            self._resolve_degeneracy()

    def _swapping_columns_and_rows(self, B_inv_N):
        basic_indices = list(zip(range(self._m), self._basic_vars))
        basic_non_art_indices = [item for item in basic_indices if item[1] < self._n]
        basic_art_indices = [item for item in basic_indices if item[1] >= self._n]

        # column swapping
        # reorder basic indices w.r.t. non basic
        basic_indices2 = basic_non_art_indices + basic_art_indices
        self._basic_vars = [x[1] for x in basic_indices2]
        # row swapping
        B_inv_N1 = np.zeros(B_inv_N.shape)
        ind2 = [x[0] for x in basic_indices2]
        for i in range(self._m):
            B_inv_N1[i, :] = B_inv_N[ind2[i], :]

        return B_inv_N1

    def _format_R12(self):
        B = self._get_submatrix_of_A1(self._basic_vars)
        non_basic_vars = list(set(range(self._n + self._m)) - set(self._basic_vars))
        N = self._get_submatrix_of_A1(non_basic_vars)
        B_inv_N = np.linalg.inv(B) @ N
        B_inv_N1 = self._swapping_columns_and_rows(B_inv_N)
        # The number of non basic, non artificial variables
        k = self._n - (self._m - self._basic_art_vars_num)
        self._R12 = B_inv_N1[:, :k]

    def _resolve_degeneracy(self):
        self._format_R12()
        # replace artificial basic columns with non-basic columns.
        self._replace_artificial_basis()

        # remove redundant rows if there exist
        rr = self._get_redundant_rows()
        if len(rr) > 0:
            self._remove_redundant_rows(rr)
            # remove redundant basis w.r.t. redundant rows.
            reserved_indices = set(range(len(self._basic_vars))) - set(rr)
            self._basic_vars = [self._basic_vars[i] for i in reserved_indices]

        print("redundant rows:", rr)
        print("basic vars:", self._basic_vars)

    def _remove_redundant_rows(self, redundant_rows):
        # remove from original instance
        reserved_rows = set(range(self._m)) - set(redundant_rows)
        self._A = np.array([self._A[i] for i in reserved_rows])
        self._b = np.array([self._b[i] for i in reserved_rows])
        self._m = len(self._A)
        # remove from ins1
        c1, A1, b1, v0 = self._ins1
        A1 = np.array([A1[i] for i in reserved_rows])
        b1 = np.array([b1[i] for i in reserved_rows])
        self._ins1 = (c1, A1, b1, v0)

    def _get_redundant_rows(self):
        # return zero-vector indices w.r.t. R2.
        k = len(self._basic_vars) - self._basic_art_vars_num
        return [i for i in range(k, self._m) if sum(np.absolute(self._R12[i])) < 1e-6]

    def _get_submatrix_of_A1(self, cols):
        """ Return the sub matrix of A1 w.r.t. column indices.
        """
        mat = []
        A = self._ins1[1]
        for j in cols:
            mat.append(A[:, j])
        return np.array(mat).transpose()

    def _replace_artificial_basis(self):

        for i in range(self._basic_art_vars_num):
            # "in" variable from non basic variables
            in_var = self._get_in_var(self._basic_art_vars_num, i)
            if in_var is None:
                continue
            # "out" variable from basic variables (which is artificial)
            out_var = self._basic_art_vars[i]

            # replacement
            for j in range(self._m):
                if self._basic_vars[j] == out_var:
                    self._basic_vars[j] = in_var
                    break

            for j in range(self._basic_art_vars_num):
                if self._basic_art_vars[j] == out_var:
                    row_ind = self._m - self._basic_art_vars_num + j
                    self._R12[:, in_var] = np.array([1 if i == row_ind else 0 for i in range(self._m)])
                    break

            print("basic vars =", self._basic_vars)
            print(np.round(self._R12, 2))
            print("======")

    def _get_in_var(self, basic_art_vars_num, art_ind):
        """
        :param basic_art_vars_num: the total number of "basic" artificial variables
        :param art_ind: the index of the artificial variable in "basic_art_vars"
        :return: "in" variable from non basic variables
        """
        row_id = self._m - basic_art_vars_num + art_ind
        k = len(self._R12[row_id])
        for j in range(k):
            if abs(self._R12[row_id][j]) > 1e-6:
                return j
        return None

    def solve(self):
        self._initialize()
        print('v0 =', self._basic_vars)
        if self._status == 'INFEASIBLE':
            print('>> INFEASIBLE.')
        else:
            print("Init: feasible.")
            sim = SimplexAD(self._c, self._A, self._b, self._basic_vars).solve()
            self._status = sim.get_status()

        return self


if __name__ == '__main__':
    from instances import instances
    ins = instances[8]  # Degenerate
    Simplex2P(ins['c'], ins['A'], ins['b']).solve()
