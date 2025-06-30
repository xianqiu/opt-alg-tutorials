import numpy as np
import copy


def shortest_paths(c):
    """ All-pairs of shortest paths
    :param c: cost matrix
        * c[i][j] = infinity if (i,j) not in E
        * c[i][j] = 0 if i = j
        * c[i][j] = cost from i to j, if (i,j) in E
    :return: shortest paths and distance matrix
    """
    n = len(c)
    # Shotrest path length
    d = np.full((n, n, n+1), np.inf)
    d[:, :, 0] = copy.copy(c)
    # Shortest paths
    p = np.empty((n, n, n+1), dtype=object)
    for i in range(n):
        for j in range(n):
            # Initialize shortest paths from i to j with length 0
            # The list contains the intermediate vertices in the shortest path
            p[i][j][0] = []

    for k in range(1, n+1):
        for i in range(n):
            for j in range(n):
                if d[i][j][k-1] > d[i][k-1][k-1] + d[k-1][j][k-1]:
                    d[i][j][k] = d[i][k-1][k-1] + d[k-1][j][k-1]
                    p[i][j][k] = p[i][k-1][k-1] + [k-1] + p[k-1][j][k-1]
                else:
                    d[i][j][k] = d[i][j][k-1]
                    p[i][j][k] = p[i][j][k-1]

    return p[:, :, n], d[:, :, n]


def print_paths(p, c):
    """
    :param p: shortest paths
    :param c: cost matrix
    """
    n = len(c)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            path = [i] + p[i][j] + [j]
            path_length = sum(c[path[k]][path[k+1]] for k in range(len(path)-1))
            print(f"({i}, {j}): path = {path}, length = {path_length}")


def random_instance(n):
    """
    :param n: number of nodes
    :return: random cost matrix
    """
    import numpy as np
    c = np.random.randint(1, 1000, (n, n))
    for i in range(n):
        c[i][i] = 0
    return c


if __name__ == '__main__':
    c = random_instance(10)
    p, _ = shortest_paths(c)
    print_paths(p, c)
   
