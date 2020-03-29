from copy import deepcopy

import numpy as np


def shortest_paths(c):
    """ 计算Graph中任意两点的最短路
    :param c: 成本矩阵
        * c[i][j] = infinity if (i,j) not in E
        * c[i][j] = 0 if i = j
        * c[i][j] = cost from i to j, if (i,j) in E
    :return: i,j之间的最短路程以及最短路
    """
    n = len(c)
    d = deepcopy(c)  # 初始化i和j之间的最短路程
    paths = init_paths(n)  # 初始化i和j之间的最短路
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    # 记录最短路
                    paths[i][j] = paths[i][k] + [k] + paths[k][j]
    return d, paths


def init_paths(n):
    """ 初始化任意两点的最短路为空list.

    :param n: 顶点的个数
    :return: n*n的list
    """
    paths = [[]] * n
    for i in range(n):
        paths[i] = [[]] * n
    return paths


def print_result(res):
    d, paths = res
    n = len(paths)
    for i in range(n):
        for j in range(i + 1, n):
            print("%d to %d:" % (i, j), str([i] + paths[i][j] + [j]), ', length:', d[i][j])


def generate_instance(n):
    c = np.random.randint(1, 1000, (n, n))
    for i in range(n):
        c[i][i] = 0
    return c


if __name__ == '__main__':
    ins = generate_instance(10)
    result = shortest_paths(ins)
    print_result(result)


