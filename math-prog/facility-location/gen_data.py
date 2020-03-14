import numpy as np
import math


class RandomData(object):
    """ 随机生成设施选址问题的例子.
    """

    def __init__(self, m, n):
        self.m = m  # 仓库数量
        self.n = n  # 客户数量

    def _cities(self):
        ub = 10 * self.n
        x = np.random.randint(1, ub, (self.n, ))
        y = np.random.randint(1, ub, (self.n, ))
        return list(zip(x, y))

    def _facilities(self):
        ub = 10 * self.n
        x = np.random.randint(1, ub, (self.m,))
        y = np.random.randint(1, ub, (self.m,))
        return list(zip(x, y))

    def _c(self):
        """ 连接成本(m*n维矩阵)
        """

        def dist(a, b):
            return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))

        return [[dist(i, j)
                 for j in self._cities()]
                for i in self._facilities()]

    def _f(self):
        """ 开仓成本(m维矩阵)
        """
        ub = 100 * self.n
        return np.random.randint(1, ub, (self.m, ))

    def generate(self):
        with open('data.py', 'w') as f:
            lines = ['[' + ', '.join(map(lambda x: ("%.4f" % x), line)) + ']' for line in self._c()]
            lines = 'C = [' + ',\n'.join(lines) + ']\n\n'
            f.writelines(lines)

            line = 'f = [' + ', '.join(map(lambda x: ("%.4f" % x), self._f())) + ']\n\n'
            f.writelines(line)
        print(">>> A random instance is generated. facility number = %d, city number = %d "
              % (self.m, self.n))


if __name__ == '__main__':
    RandomData(50, 200).generate()
