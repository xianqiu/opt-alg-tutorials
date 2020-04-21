
def choose_exact(n, k):
    """
    从n个物品[0, 1, ... n-1]里选择k个, 枚举所有情况. 例如:
    >>> choose_exact(4, 2)
    [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    >>> choose_exact(3, 3)
    [[0, 1, 2]]
    """
    if k == 1:
        return [[i] for i in range(n)]
    res_mid = choose_exact(n, k - 1)
    result = []
    for p in res_mid:
        for i in range(max(p) + 1, n):
            result.append(p + [i])
    return result


def choose_at_most(n, k):
    """ 从n个物品[0, 1, ..., n-1]里选择至少1个至多k个, 枚举所有情况.
    """
    result = []
    for i in range(1, k + 1):
        result += choose_exact(n, i)
    return result


class KnapsackPTAS(object):
    """
    背包问题的PTAS.
    近似比: OPT/ALG <= (1+1/k), 计算时间复杂度 = O(kn^{k+1}).
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

    def solve(self, k):
        # step1. 枚举所有不超过k个物品的解, 取价值最大的可行解
        solutions = choose_at_most(self._n, k)
        max_sol = None
        max_p = 0
        for sol in solutions:
            if sum([self._w[i] for i in sol]) > self._W:
                continue
            p = sum([self._p[i] for i in sol])
            if p > max_p:
                max_p = p
                max_sol = sol
        # step2. 背包的剩余空间用贪心算法填充
        self._result = self._greedy(max_sol)
        return self

    def _greedy(self, sol):
        """
        给定可行解sol, 把背包剩余的空间用贪心算法填充.
        """

        # 背包剩余的空间
        available_space = self._W - sum([self._w[i] for i in sol])
        new_items = []
        # 剩下的物品
        left_over = set(range(self._n)) - set(sol)
        # 计算剩下物品的性价比
        left_over_values = [self._p[i] / self._w[i] for i in left_over]
        # 按性价比从大到小排序
        left_over_items = sorted(zip(left_over, left_over_values), key=lambda x: x[1], reverse=True)
        left_over = [item[0] for item in left_over_items]
        # 把剩余的物品依次装入背包(如果能装下)
        for i in left_over:
            if self._w[i] <= available_space:
                new_items.append(i)
                available_space -= self._w[i]

        return sol + new_items

    def print_result(self):
        print("Packed items:", self._result)
        print("Total profit:", sum([self._p[i] for i in self._result]))
        print("Total weight:", sum([self._w[i] for i in self._result]))


if __name__ == '__main__':
    W = 67
    p = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    w = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]

    knapsack = KnapsackPTAS(w, p, W).solve(5)
    knapsack.print_result()
