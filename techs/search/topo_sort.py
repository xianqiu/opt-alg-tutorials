from techs.search.dfs import DFS


class TopologicalSort(object):
    """ Apply depth-first-search to topological sort.
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
        self._G1 = {}  # 拓扑排序结果

    def run(self):
        d = DFS(self._G).run()
        f = d.get_finishing_times()
        # 把顶点按finishing time排序(降序)
        items_sorted = list(sorted(f.items(), key=lambda x: x[1], reverse=True))
        # 顶点到编号的映射
        m = {items_sorted[i][0]: i for i in range(len(items_sorted))}
        # 拓扑排序
        for u, edges in self._G.items():
            self._G1[m[u]] = [m[v] for v in edges]
        return self

    def print_result(self):
        for v, edges in self._G1.items():
            print(v, "->", edges)


if __name__ == '__main__':
    G = {
        1: [2, 3, 4],
        2: [5, 3, 6],
        3: [4, 6],
        4: [7],
        5: [3, 6],
        6: [],
        7: []
    }

    t = TopologicalSort(G).run()
    t.print_result()
