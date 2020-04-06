import math


class BFS(object):
    """ Breadth-first-search.
    得到搜索树和最短路(边权=1).
    """

    def __init__(self, G, s):
        """
        :param G: Graph, 数据结构为邻接表:
            key = node index, value = list of adjacent node indices, e.g.,
        {
            0: [...]  # node 0
            1: [...]  # node 1
            ...
        }
        :param s: 搜索的初始点的编号, int
        """
        self._G = G
        self._s = s
        self._d = self._init_distances()
        # colors
        # white-未被发现
        # gray-发现但未发现它所有邻接点
        # black-发现它以及所有的邻接点
        self._c = {v: 'white' for v in self._G.keys()}
        # 记录搜索树
        self._p = {}  # key = node, value = parent

    def _init_distances(self):
        d = {v: math.inf for v in self._G.keys()}
        d[self._s] = 0
        return d

    def run(self):
        q = [self._s]
        self._c[self._s] = 'gray'
        while len(q):
            u = q.pop(0)
            # 考虑u的所有邻边(u, v)
            for v in self._G[u]:
                if self._c[v] == 'white':
                    self._d[v] = self._d[u] + 1
                    self._p[v] = u
                    self._c[v] = 'gray'
                    q.append(v)
            self._c[u] = 'black'

    def print_path(self, s, v):

        def format_path(node, path):
            if node == s:
                path.append(str(s))
                return
            elif node in self._p.keys():
                format_path(self._p[node], path)
                path.append(str(node))

        res = []
        format_path(v, res)
        print(' -> '.join(res), "total distance:", self._d[v])


if __name__ == '__main__':
    G = {
        0: [1, 4],
        1: [0, 5],
        2: [3, 5, 6],
        3: [2, 6, 7],
        4: [0],
        5: [1, 2, 6],
        6: [2, 3, 5, 7],
        7: [3, 6]
    }

    b = BFS(G, 1)
    b.run()
    b.print_path(1, 3)



