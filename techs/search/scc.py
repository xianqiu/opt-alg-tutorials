from techs.search.dfs import DFS


class SCC(object):
    """
    Compute strongly connected components (SCC).
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
        self._scc = None  # 计算结果

    @staticmethod
    def _transpose(G):
        """ 计算G的转置(Transpose graph).
        """
        G_t = {v: [] for v in G.keys()}
        for u, edges in G.items():
            for v in edges:
                G_t[v].append(u)
        return G_t

    def run(self):
        # step1: Apply DFS to G
        d1 = DFS(self._G).run()
        f = d1.get_finishing_times()
        # 把顶点按finishing time排序(降序)
        items_sorted = sorted(f.items(), key=lambda x: x[1], reverse=True)
        # step2: Apply DFS to the transpose of G
        vertices = [item[0] for item in items_sorted]
        d2 = DFS(self._transpose(self._G)).run(vertices)
        # format result
        forest = d2.get_search_forest()
        self._scc = self._format_scc(forest)
        return self

    @staticmethod
    def _format_scc(forest):
        """ 计算搜索森林中每颗树的顶点集合.
        """
        scc = []
        for tree in forest:
            tree_vertices = set({})
            for k, v in tree.items():
                tree_vertices.add(k)
                if v:
                    tree_vertices.add(v)
            scc.append(tree_vertices)

        return scc

    def print_result(self):
        print("Strongly connected components:")
        print(self._scc)


if __name__ == '__main__':
    G = {
        1: [2],
        2: [3, 5, 6],
        3: [4, 7],
        4: [3, 8],
        5: [1, 6],
        6: [7],
        7: [6, 8],
        8: [8]
    }

    s = SCC(G).run()
    s.print_result()
