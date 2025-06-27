class TSP2opt(object):

  def __init__(self, d):
      """
      :param d: distance matrix
      """
      self._d = d
      self._iter = 0  # iteration count
      self._result = None
      self._result_length = 0
      self._tours = []

  def _init_tour(self):
      n = len(self._d)
      return [(i, i+1) for i in range(n-1)] + [(n-1, 0)]

  @staticmethod
  def _apply_2opt(tour, i, j):
      """ Apply 2opt to arc i and j.
      :param tour: list of arcs, e.g. tour of 4 vertices: [(0, 1), (1, 2), (2, 3), (3, 0)]
      :param i: arc i of the tour
      :param j: arc j of the tour.
      :return: a new tour (feasible solution)
      """
      u, v = tour[i]
      s, t = tour[j]
      part1 = tour[0:i]
      part2 = [(u, s)]
      part3 = [(tour[i+j-k][1], tour[i+j-k][0])for k in range(i+1, j)]
      part4 = [(v, t)]
      part5 = tour[j+1:]
      return part1 + part2 + part3 + part4 + part5

  def _is_2opt_make_improvement(self, tour, i, j):
      """
      Given a tour, assess whether applying 2opt(i,j) can make the tour shorter.
      """
      u, v = tour[i]
      s, t = tour[j]
      if self._d[u][v] + self._d[s][t] > self._d[u][s] + self._d[v][t]:
          return True
      return False

  def _get_tour_length(self, tour):
      return sum([self._d[i][j] for (i, j) in tour])

  def solve(self, max_iter=10000):
      n = len(self._d)
      self._result = self._init_tour()
      self._result_length = self._get_tour_length(self._result)
      self._tours.append(self._result)  # 记录中间结果

      improvement = 1
      while improvement >= 1:
          s0 = self._result_length
          for i in range(n):
              for j in range(i+1, n):
                  if self._iter == max_iter:
                      return self
                  if self._is_2opt_make_improvement(self._result, i, j):
                      self._result = self._apply_2opt(self._result, i, j)
                      self._tours.append(self._result)
                      self._result_length = self._get_tour_length(self._result)
                      print("iter = %d, tour length = %d" %
                            (self._iter, self._get_tour_length(self._result)))
                      self._iter += 1
          improvement = self._result_length - s0

      return self

  def print_result(self):
      print("==== result ====")
      print("tour:", [arc[0] for arc in self._result])
      print("tour length:", self._result_length)

  def get_tours(self):
      """
      :return: all tours during the search process.
      """
      return self._tours


if __name__ == '__main__':
    import numpy as np
    d = np.random.randint(1, 100, (10, 10))
    tsp = TSP2opt(d)
    tsp.solve()
    tsp.print_result()