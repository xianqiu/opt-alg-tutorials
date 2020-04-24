import json
from pathlib import Path

import pyproj
import numpy as np


class CityLocations(object):
    # 注意: 高德坐标系
    city_locations = {
        '石家庄': (114.51486, 38.042307),
        '沈阳': (123.431474, 41.805698),
        '哈尔滨': (126.534967, 45.803775),
        '杭州': (120.15507, 30.274084),
        '福州': (119.296494, 26.074507),
        '济南': (117.119999, 36.651216),
        '广州': (113.264434, 23.129162),
        '武汉': (114.305392, 30.593098),
        '成都': (104.066541, 30.572269),
        '昆明': (102.832891, 24.880095),
        '兰州': (103.834303, 36.061089),
        '南宁': (108.366543, 22.817002),
        '银川': (106.230909, 38.487193),
        '太原': (112.548879, 37.87059),
        '长春': (125.323544, 43.817071),
        '南京': (118.796877, 32.060255),
        '合肥': (117.227239, 31.820586),
        '南昌': (115.858197, 28.682892),
        '郑州': (113.625368, 34.746599),
        '长沙': (112.938814, 28.228209),
        '海口': (110.198293, 20.044001),
        '贵阳': (106.630153, 26.647661),
        '西安': (108.940174, 34.341568),
        '西宁': (101.778228, 36.617144),
        '呼和浩特': (111.74918, 40.842585),
        '拉萨': (91.140856, 29.645554),
        '乌鲁木齐': (87.616848, 43.825592),
        '北京': (116.407526, 39.90403),
        '上海': (121.473701, 31.230416),
        '重庆': (106.551556, 29.563009),
        '天津': (117.200983, 39.084158)
    }

    @property
    def locations(self):
        return list(self.city_locations.values())

    def to_js(self):
        """ 把数据保存成js文件. path = 'web/data_cities.js'
        """
        data_js = [{'name': name, 'coordinates': loc}
                   for (name, loc) in self.city_locations.items()]
        path = Path('web') / 'data_cities.js'
        var_name = 'S.data.cities'
        with open(path, 'w', encoding='utf-8') as f:
            f.write('%s = %s;' % (var_name, json.dumps(data_js)))

    @staticmethod
    def _polar_to_plane(points):
        """ 把经纬度坐标投影到二维平面.
        """
        p = pyproj.Proj(4508)
        return [p(point[0], point[1]) for point in points]

    def get_distance_matrix(self):
        loc_plane = self._polar_to_plane(self.city_locations.values())

        def calc_distance(i, j):
            x1, y1 = loc_plane[i]
            x2, y2 = loc_plane[j]
            return int(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

        n = len(loc_plane)
        return [[calc_distance(i, j) for j in range(n)] for i in range(n)]
