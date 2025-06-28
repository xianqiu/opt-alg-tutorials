class TSP2opt(object):

    max_iter = 1000

    def __init__(self, d):
        """
        :param d: distance matrix
        """
        self._d = d
        self._n = len(d)
        self._iter = 0
        # Start with a trivial solution.
        self.tour = [(i, i+1) for i in range(self._n-1)] + [(self._n-1, 0)]

    def _2opt(self, i, j):
        """ Search with 2opt. If a better solution is found, update the current tour.
        :param i: index of the tour, indicating self.tour[i]
        :param j: index of the tour, indicating self.tour[j]
        :return: True if a better solution is found, False otherwise
        """
        u, v = self.tour[i]
        s, t = self.tour[j]
        part1 = self.tour[0: i]
        part2 = [(u, s)]
        part3 = [(self.tour[i + j - k][1], self.tour[i + j - k][0]) for k in range(i + 1, j)]
        part4 = [(v, t)]
        part5 = self.tour[j + 1: ]
        new_tour = part1 + part2 + part3 + part4 + part5
        new_tour_length = sum([self._d[i][j] for (i, j) in new_tour])
        if new_tour_length < self.tour_length:
            self.tour = new_tour
            return True
        return False

    @property
    def tour_length(self):
        return sum([self._d[i][j] for (i, j) in self.tour])

    def _print_iter(self):
        print(">> iter = %d, tour length = %d" % (self._iter, self.tour_length))

    def solve(self):
        is_improved = True
        while is_improved:
            current_length = self.tour_length
            for i in range(self._n):
                for j in range(i + 1, self._n):
                    if self._2opt(i, j):
                        self._iter += 1
                        self._print_iter()
                        if self._iter == self.max_iter:
                            return self

            is_improved = current_length - self.tour_length > 0

        return self


if __name__ == '__main__':
    import numpy as np
    n = 100  # number of cities
    d = np.random.randint(1, 1000, (n, n))
    tsp = TSP2opt(d)
    tsp.solve()
