class DFS(object):
    """ Depth First Search
    """

    def __init__(self, G):
        """
        :param G: Graph, 数据结构为邻接表:
            key = node index, value = list of adjacent node indices, e.g.,
        {
            0: [...]  # node 0
            1: [...]  # node 1
            ...
        }
        """
        self._G = G
        # colors
        # white-未被发现
        # gray-发现但未发现它所有邻接点
        # black-发现它以及所有的邻接点
        self._c = {v: 'white' for v in self._G.keys()}
        self._time = 0
        # discovering time
        self._d = {v: 0 for v in self._G.keys()}
        # finishing time
        self._f = {v: 0 for v in self._G.keys()}
        # 记录搜索森林
        # list of dict: key = node, value = parent
        self._forest = []

    def _traverse(self, u, p):
        """ DFS.
        :param u: 搜索的初始顶点编号, int
        :param p: 用来记录搜索树, dict, key = node, value = parent
        注意: 如果搜索树只是一个孤立点, 结果不会保存在p中.
        """
        self._time += 1
        self._c[u] = 'gray'  # 发现u, 标记为灰色
        self._d[u] = self._time  # 记录发现时间
        for v in self._G[u]:  # 考虑所有(u,v)
            if self._c[v] == 'white':
                p[v] = u
                self._traverse(v, p)
        self._time += 1
        self._c[u] = 'black'  # 结束u, 标记为黑色
        self._f[u] = self._time  # 记录结束时间
        # 孤立点
        if not p:
            p[u] = None

    def run(self, vertices=None):
        """
        :param vertices: list, 按照列表中顶点的顺序执行DFS.
        """
        if not vertices:
            vertices = self._G.keys()
        for u in vertices:
            p = {}
            if self._c[u] == 'white':
                self._traverse(u, p)
            if p:
                self._forest.append(p)
        return self

    def get_finishing_times(self):
        return self._f

    def get_discovering_times(self):
        return self._d

    def get_search_forest(self):
        return self._forest


if __name__ == '__main__':
    G = {
        0: [1, 3],
        1: [4],
        2: [4, 5],
        3: [1],
        4: [3],
        5: [5],
        6: [6]
    }

    d = DFS(G).run()
    print("discovering times:", d.get_discovering_times())
    print("finishing times:", d.get_finishing_times())
    print("search forest:", d.get_search_forest())
