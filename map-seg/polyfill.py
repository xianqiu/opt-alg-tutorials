from shapely.geometry import Polygon, MultiPolygon, Point
import matplotlib.pyplot as plt
import numpy as np


class PolyGetter(object):
    """ 生成正多边形对象
    """

    def __init__(self, radius, k, theta=0.0):
        self.radius = radius  # 半径
        self.k = k  # 正多边形的边数
        self.theta = theta  # 起始角度: degree

    def from_center(self, center):
        """ 输入中心点的坐标，返回对应的正多边形
        :param center: Point对象
        """
        def get_xy(i):
            x = center.x + self.radius * np.cos(2 * np.pi * (i / self.k + self.theta / 360))
            y = center.y + self.radius * np.sin(2 * np.pi * (i / self.k + self.theta / 360))
            return x, y

        return Polygon([Point(get_xy(i)) for i in range(self.k)])

    @staticmethod
    def _get_mirror(point, line):
        """ 计算 point 关于直线的对称点
        :param point: (x0, y0)
        :line: (x1, y1, x2, y2)
        :return: (x, y)
        """
        x0, y0 = point
        x1, y1, x2, y2 = line
        if abs(x2 - x1) > 1e-6:
            k = (y2 - y1) / (x2 - x1)
            d = (k * x0 - y0 + y1 - k * x1) / (k ** 2 + 1)
            x = x0 - 2 * k * d
            y = y0 + 2 * d
        else:  # 斜率正无穷（垂直线）
            x = x0 + 2 * (x1 - x0)
            y = y0
        return x, y

    def _get_neighbor(self, center, vertex):
        x0, y0 = center
        eta = (vertex[0] - x0) / self.radius
        if abs(eta) > 1:  # 浮点数问题，有可能出现 1.000000000001
            eta = np.round(eta, 6)
        theta = np.arccos(eta)
        if vertex[1] - y0 < 0:
            theta = -theta

        coords = []
        delta = 2 * np.pi / self.k
        for i in range(self.k):
            x = x0 + self.radius * np.cos(theta + i * delta)
            y = y0 + self.radius * np.sin(theta + i * delta)
            coords.append((x, y))
        return Polygon(coords)

    def neighbors_of(self, poly):
        """ 输入正多边形，返回它所有邻接的多边形
        :param poly: 多边形，Polygon对象
        """
        # 四边形和六边形的情况
        # self._neighbors_of_fast 算得快一些
        if self.k == 4 or self.k == 6:
            return self._neighbors_of_fast(poly)
        # 通用情况（算得慢一些）
        center = (poly.centroid.x, poly.centroid.y)
        coords = list(poly.exterior.coords)
        res = []
        for i in range(self.k):
            line = list(coords[i]) + list(coords[i+1])
            mirror = self._get_mirror(center, line)
            p = self._get_neighbor(mirror, coords[i])
            res.append(p)
        return res

    def _neighbors_of_fast(self, poly):
        """ 输入正多边形，返回它所有邻接的多边形
            **注意** 仅对 k= 4, 6 有效（三角形无效）
        :param poly: 多边形，Polygon对象
        """
        dist = self.radius * np.cos(np.pi / self.k)  # 计算中心到边的距离
        p = PolyGetter(2 * dist,
                       self.k,
                       self.theta + 180 / self.k)
        centers = list(p.from_center(poly.centroid).exterior.coords)
        return [Polygon(self.from_center(Point(c))) for c in centers]


class PolyFill(object):
    """ 给定一个多边形区域, 用正多边形填充它.
    """

    def __init__(self, boundary, center):
        """
        :param boundary: 被分割的多边形 [(x0,y0), (x1, y1), ...]
        :param center: 锚点 [x, y]，以center为出发点进行填充
        """
        # 输入
        self._boundary = boundary
        if not isinstance(self._boundary, Polygon):
            self._boundary = Polygon(self._boundary)
        self._center = center
        if not isinstance(self._center, Point):
            self._center = Point(self._center)
        self._radius = None
        self._k = None
        self._theta = None
        # 输出
        # [[(x11, y11), (x12, y12)...]  # 多边形1
        #  [(x21, y21), (x22, y22)...]  # 多边形2
        #     ...]  # ...
        self._result = []  # 保存为多边形的顶点坐标集合
        # 辅助变量
        self._poly_getter = None
        self._res_polys = []  # 填充结果（保存为多边形对象）
        # 用来保存已经搜索过的正多边形（用中心点来表示）
        self._searched_polys = set({})

    def set_params(self, radius, k=6, theta=0):
        """ 参数设置.
        :param radius: 正多边形外接圆的半径
        :param k: 正k多边形.  k = 3, 4, 6
        :param theta: 正多边形的起始角度（度数）
        """
        self._radius = radius
        self._k = k
        self._theta = theta
        assert radius > 0 and k in {3, 4, 6}, \
            ValueError('radius > 0 and k in (3, 4, 6)')
        self._radius = radius
        self._k = k
        self._theta = theta
        self._poly_getter = PolyGetter(self._radius, self._k, self._theta)

        return self

    def get_result(self):
        return self._result

    def show(self):
        # draw polygons
        for points in self._result:
            plt.plot(*list(zip(*points)))
        # draw center
        plt.plot(self._center.x, self._center.y, 'x')
        # draw boundary
        plt.plot(*list(zip(*self._boundary.exterior.coords)))
        plt.axis('equal')
        plt.show()

    def fill(self):
        assert self._radius, ValueError("set parameters first!")
        # 生成多边形对象
        start_poly = self._poly_getter.from_center(self._center)
        # 以start_poly为起点执行BFS填充boundary
        self._fill_by_bfs(start_poly)
        self._result = [list(poly.exterior.coords) for poly in self._res_polys]
        return self

    def _fill_by_bfs(self, start_poly):
        """ 给定初始的填充多边形, 按照BFS的方式填充周围的区域
        以k多边形为例(k=3,4,6), 有k个多边形与它相邻
        """
        self._mark_as_searched(start_poly)
        q = [start_poly]
        while len(q):
            poly = q.pop(0)
            self._append_to_result(poly)
            # 把有效的多边形加入队列. 有效的定义:
            # 1. 与poly邻接;
            # 2. 未被搜索过;
            # 3. 在边界内（与boundary定义的区域有交集)
            q += self._get_feasible_neighbors(poly)

    def _mark_as_searched(self, poly):
        """ 把多边形标记为'已搜索'
        """
        self._searched_polys.add(self._get_poly_id(poly))

    @staticmethod
    def _get_poly_id(poly):
        """ 用多边形的中心点的位置判断两个多边形是否相同
        注意浮点数精度问题
        """
        c = poly.centroid
        return '%.2f,%.2f' % (c.x, c.y)

    def _is_searched(self, poly):
        """ 判断多边形是否存在
        """
        return self._get_poly_id(poly) in self._searched_polys

    def _append_to_result(self, poly):
        """ 把正多边形poly保存到结果集
        """
        # poly与boundary取交集, 然后保存结果
        s = self._boundary.intersection(poly)
        if s.is_empty:
            return
        # Polygon对象则直接保存
        if isinstance(s, Polygon):
            self._res_polys.append(s)
        # MultiPolygon对象则依次把它包含的Polygon对象保存
        elif isinstance(s, MultiPolygon):
            for p in s:
                self._res_polys.append(p)

    def _get_feasible_neighbors(self, poly):
        """ 计算与poly邻接的有效的正多边形, 然后标记为'已搜索'
        """
        def mark_searched(p):
            self._mark_as_searched(p)
            return p

        def is_feasible(p):
            if self._is_searched(p) or self._boundary.intersection(p).is_empty:
                return False
            return True

        # 1. 仅包含'未被搜索'和'不在界外'的正多边形
        # 2. 把poly所有的feasible多边形标记为'已搜索'
        return [mark_searched(p)
                for p in self._poly_getter.neighbors_of(poly)
                if is_feasible(p)]


if __name__ == '__main__':

    def generate_boundary():
        # 生成一个半径为10的正四边形
        return PolyGetter(radius=10, k=4, theta=45).from_center(Point(0, 0))

    pf = PolyFill(generate_boundary(), center=Point(0, 0))
    pf.set_params(radius=1.5, k=6)  # 正六边形填充
    # pf.set_params(radius=1.5, k=4)  # 正方形填充
    # pf.set_params(radius=1.5, k=3)  # 正三角形填充
    pf.fill().show()

