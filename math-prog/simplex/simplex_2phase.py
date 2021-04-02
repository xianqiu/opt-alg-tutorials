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
        self._ins1 = self._construct_phase1_instance()

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
        basic_vars = sim.get_basic_vars()

        # Case2(degenerate): artificial vars in basic vars.
        # Then exchange artificial columns with non-basic columns.
        if self._is_degenerate(basic_vars):
            basic_vars = self._resolve_degeneracy(basic_vars)

        return basic_vars

    def _is_degenerate(self, basic_vars):
        for i in basic_vars:
            if i >= self._n:
                return True
        return False

    def _resolve_degeneracy(self, basic_vars):
        # basic artificial variables
        basic_art_vars = [i for i in basic_vars if i >= self._n]
        # remove redundant rows if there exist
        rr = self._get_redundant_rows(basic_art_vars)
        if len(rr) > 0:
            self._remove_redundant_rows(rr)
            # remove redundant basis w.r.t. redundant rows.
            reserved_indices = set(range(len(basic_vars))) - set(rr)
            basic_vars = [basic_vars[i] for i in reserved_indices]
        # replace artificial basic columns with non-basic columns.
        self._replace_art_basis(basic_vars, basic_art_vars)

        return basic_vars

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

    def _get_redundant_rows(self, basic_artificial_vars):
        A2 = self._get_submatrix_of_A1(basic_artificial_vars)
        m = len(A2)
        # return zero-vector indices w.r.t. A2.
        return [i for i in range(m) if sum(A2[i]) < 1e-6]

    def _get_submatrix_of_A1(self, cols):
        """ Return the sub matrix of A1 w.r.t. column indices.
        """
        mat = []
        A = self._ins1[1]
        for j in cols:
            mat.append(A[:, j])
        return np.array(mat).transpose()

    def _replace_art_basis(self, basic_vars, basic_art_vars):
        non_basic_vars = set(range(self._n)) - set(basic_vars)
        s = len(basic_art_vars)
        for i in range(s):
            # "in" variable from non basic variables
            in_var = self._get_in_var(non_basic_vars, s, i)
            # "out" variable from basic variables (which is artificial)
            out_var = basic_art_vars[i]
            # replacement
            for j in range(len(basic_vars)):
                if basic_vars[j] == out_var:
                    basic_vars[j] = in_var

    def _get_in_var(self, non_basic_vars, basic_art_vars_num, art_ind):
        """
        :param non_basic_vars: non basic variables
        :param basic_art_vars_num: the total number of "basic" artificial variables
        :param art_ind: the index of the artificial variable in "basic_art_vars"
        :return: "in" variable from non basic variables
        """
        row_id = self._m - basic_art_vars_num + art_ind
        A1 = self._ins1[1]
        for j in non_basic_vars:
            if A1[row_id][j] > 1e-6:
                return j

    def solve(self):
        v0 = self._initialize()

        if self._status == 'INFEASIBLE':
            print('>> INFEASIBLE.')
        else:
            print("Init: feasible.")
            sim = SimplexAD(self._c, self._A, self._b, v0).solve()
            self._status = sim.get_status()

        return self