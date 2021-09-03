import numpy as np
from copy import deepcopy

from ortools.linear_solver import pywraplp


class Node(object):
    """ LP relaxation model.
    """

    def __init__(self, c, A, b, lb, ub):
        self._c = c
        self._A = A
        self._b = b
        self.lb = lb
        self.ub = ub
        self._sol = None
        self._obj_val = None

    def _create_model(self):
        """ 根据输入，初始化模型。
        """
        model = pywraplp.Solver.CreateSolver('GLOP')
        m, n = len(self._b), len(self._c)
        # 决策变量
        x = [model.NumVar(self.lb[j], self.ub[j], 'x[%d]' % j) for j in range(n)]
        # 约束: Ax <= b
        for i in range(m):
            ct = model.Constraint(-model.infinity(), self._b[i])
            for j in range(n):
                ct.SetCoefficient(x[j], self._A[i][j])
        # 目标
        obj = model.Objective()
        for j in range(n):
            obj.SetCoefficient(x[j], self._c[j])
        obj.SetMaximization()
        return model, x, obj

    def solve(self):
        """ 求解模型
        """
        model, x, obj = self._create_model()
        status = model.Solve()
        if status == model.OPTIMAL or status == model.FEASIBLE:
            self._sol = [x[j].solution_value() for j in range(len(x))]
            self._obj_val = obj.Value()
        return status

    def get_sol(self):
        return self._sol

    def get_obj_val(self):
        return self._obj_val


def _get_children(v: Node, branch_ind: int):
    """ 计算分支节点(其中 i = brand_id)：
        x[i] <= d,
        x[i] >= d+1
        只需要重新设置lb[i]和ub[i]
    """
    d = int(v.get_sol()[branch_ind])
    # left child
    # Python对象是指针引用，所以用深拷贝
    left_child = deepcopy(v)
    left_child.ub[branch_ind] = d
    # right child
    right_child = deepcopy(v)
    right_child.lb[branch_ind] = d+1
    return left_child, right_child


class BranchBound(object):
    """ 分支定界法 (Branch and bound method)
    注意：
    1、最大化问题。
    2、整数规划。
    3、决策变量非负。
    """

    def __init__(self, c, A, b, lb=None, ub=None):
        """
        :param c: n * 1 vector
        :param A: m * n matrix
        :param b: m * 1 vector
        :param lb: list, lower bounds of x, e.g. [0, 0, 1, ...]
        :param ub: list, upper bounds of x, e.g. [None, None, ...], None 代表正无穷
        """
        self._c = c
        self._A = A
        self._b = b
        self._lb = lb
        self._ub = ub
        self._m = len(A)
        self._n = len(c)
        self._sol = None  # 决策变量的值
        self._obj_val = -np.inf  # 目标函数值

    def _init_lb_ub(self):
        if self._lb is None:
            self._lb = [0] * self._n
        if self._ub is None:
            self._ub = [pywraplp.Solver.Infinity()] * self._n
        else:
            for j in range(self._n):
                if self._ub[j] is None:
                    self._ub[j] = pywraplp.Solver.Infinity()

    def _init_node(self):
        self._init_lb_ub()
        return Node(self._c, self._A, self._b, self._lb, self._ub)

    def _get_branch_ind(self, sol):
        """ 计算解的非整数分量（的下标），用来分支。
        """
        for i in range(self._n):
            if abs(sol[i]-np.floor(sol[i])) > 1e-6:
                return i
        return None

    def _solve_dfs(self, v: Node):
        """ 给定节点v，采用深度优先，搜索v的子树。
        """
        status = v.solve()
        if status == pywraplp.Solver.INFEASIBLE:
            return
        sol = v.get_sol()
        val = v.get_obj_val()
        # bounding
        if val < self._obj_val:
            return
        # branching
        branch_ind = self._get_branch_ind(sol)
        if branch_ind is not None:
            c1, c2 = _get_children(v, branch_ind)
            self._solve_dfs(c1)
            self._solve_dfs(c2)
        # 更新结果
        elif val > self._obj_val:
            self._sol = sol
            self._obj_val = val

    def solve(self):
        v0 = self._init_node()
        self._solve_dfs(v0)
        print("solution =", b.get_solution())
        print("objective value =", b.get_obj_val())

    def get_obj_val(self):
        return self._obj_val

    def get_solution(self):
        return self._sol


if __name__ == '__main__':
    from instances import instances
    ins = instances[2]
    b = BranchBound(ins['c'], ins['A'], ins['b'],
                    lb=ins['lb'],
                    ub=ins['ub'])
    b.solve()

