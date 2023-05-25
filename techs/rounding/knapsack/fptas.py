import math


class KnapsackDP(object):
    """ 背包问题的动态规划算法.
    """

    def __init__(self, w, p, W):
        """
        :param w: 物品大小, list
        :param p: 物品价值, list
        :param W: 背包大小, int
        """
        self._w = w
        self._p = p
        self._W = W
        self._n = len(self._w)
        self._f = self._init_recurrence_formula()
        self._result = None

    def _init_recurrence_formula(self):
        n = len(self._w)
        f = [[]] * n
        max_p = max(self._p)
        for i in range(n):
            f[i] = [math.inf] * n * max_p
        f[0][0] = 0  # !
        f[0][self._p[0]] = self._w[0]
        return f

    def solve(self):
        n = len(self._w)
        max_p = max(self._p)

        # key = profit, value = 达到此profit所包含的一个item
        for i in range(n-1):
            for j in range(n * max_p):
                if self._p[i+1] <= j:
                    self._f[i+1][j] = min(self._f[i][j],
                                          self._f[i][j-self._p[i+1]] + self._w[i+1])
                    
                else:
                    self._f[i+1][j] = self._f[i][j]

        self._result = self._get_result( self._get_profit())
        return self

    def _get_profit(self):
        weights = self._f[len(self._w) - 1]
        # print(weights)
        m = len(weights)
        for i in range(m):
            value = m - 1 - i
            if weights[value] <= self._W:
                return value

    def _get_result(self,  profit):
        result = []
        for i in range(self._n-1,0,-1):
            if self._f[i][profit] > self._f[i-1][profit] or self._f[i-1][profit] == math.inf:
                result.append(i)
                profit -= self._p[i]
        return result

    def get_result(self):
        return self._result

    def print_result(self):
        print("Packed items:", self._result)
        print("Total profit:", sum([self._p[i] for i in self._result]))
        print("Total weight:", sum([self._w[i] for i in self._result]))


class KnapsackFPTAS(object):
    """ 动态规划FPTAS.
    近似比: ALG >= (1-epsilon)OPT, 时间复杂度 = O(n^2 * floor(n/epsilon))
    """
    def __init__(self, w, p, W):
        """
        :param w: 物品大小, list
        :param p: 物品价值, list
        :param W: 背包大小, int
        """
        self._w = w
        self._p = p
        self._W = W
        self._n = len(self._w)
        self._result = None

    def solve(self, epsilon):
        k = epsilon * max(self._p) / len(self._w)
        p1 = [int(x/k) for x in self._p]
        dp = KnapsackDP(self._w, p1, self._W).solve()
        self._result = dp.get_result()
        return self

    def print_result(self):
        print("Packed items:", self._result)
        print("Total profit:", sum([self._p[i] for i in self._result]))
        print("Total weight:", sum([self._w[i] for i in self._result]))


if __name__ == '__main__':
    W = 180 #150
    p = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    w = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]
    import time
    print("==== DP solution ====")
    t1 = time.time()
    knapsack = KnapsackDP(w, p, W).solve()
    print(">> time cost:", time.time() - t1)
    knapsack.print_result()
    print("==== FPTAS solution ====")
    t1 = time.time()
    p = KnapsackFPTAS(w, p, W).solve(0.5)
    print(">> time cost:", time.time() - t1)
    p.print_result()