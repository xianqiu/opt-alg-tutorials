from pathlib import Path
import json
import webbrowser

from shapely.geometry import Polygon
from pyproj import Proj

from polyfill import PolyFill


def project_to_plane(points):
    """ 把物理点投影到二维平面
    """
    p = Proj(4508)
    return [p(point[0], point[1]) for point in points]


def project_to_polar(points):
    """ 把平面上的点转换成极坐标
    """
    p = Proj(4508)

    def proj_and_round(point):
        q = p(point[0], point[1], inverse=True)
        return round(q[0], 6), round(q[1], 6)

    return [proj_and_round(point) for point in points]


def to_js(points, path, var_name):
    """ 保存成js文件（前端展示）
    """
    data_js = {
        'coordinates': [list(p) for p in points]
    }
    with open(path, 'w', encoding='utf-8') as f:
        f.write('%s = [%s];' % (var_name, json.dumps(data_js)))


class MapSeg(object):
    """ 用正多边形分割地图区域
    """

    def __init__(self, coordinates):
        """
        :param coordinates: [(x0,y0), (x1,y1), ...]
        """
        self._coordinates = coordinates
        self._radius = None
        self._k = None
        self._theta = None

    def set_params(self, radius, k, theta=0):
        """ 参数设置
        """
        self._radius = radius  # 半径
        self._k = k  # 正多边形的边数 k = 3, 4, 6
        self._theta = theta  # 初始的角度
        return self

    def segment(self):
        """ 用PolyFill分割地图，并展示结果
        """
        # 把经纬度投影到二位平面
        boundary_plane = Polygon(project_to_plane(self._coordinates))
        # 用正多边形填充
        pf = PolyFill(boundary_plane, boundary_plane.centroid)
        pf.set_params(self._radius, self._k, self._theta)
        result = pf.fill().get_result()
        # 把结果转换成极坐标
        result = [project_to_polar(poly) for poly in result]
        # 保存结果：写到js文件中
        directory = Path('web')
        to_js(self._coordinates, directory / 'data_boundaries.js', 'MS.data.blockBoundaries')
        to_js(result, directory / 'data_bricks.js', 'MS.data.bricks ')
        # 打开 web 文件夹下的 index.html
        # 查看可视化的结果
        # 如果没有自动弹出网页，可以手动打开 ./web/index.html
        path = directory.absolute() / 'index.html'
        webbrowser.open('file://' + str(path))


if __name__ == '__main__':
    import data
    # 杭州市西湖区的边界
    coord = data.boundary_district_330106
    ms = MapSeg(coord)
    ms.set_params(radius=2000, k=6).segment()  # 六边形分割（半径2000米）
    # ms.set_params(radius=2000, k=4).segment()  # 四边形分割
    # ms.set_params(radius=2000, k=3).segment()  # 三角形分割
