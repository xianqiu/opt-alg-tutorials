import logging

import requests


class AMap(object):

    """ 用高德地图提供的API获取"地区"边界
    """

    def __init__(self, key):
        self._key = key

    @staticmethod
    def _request(url, params):
        try:
            response = requests.get(url, params)
            if response.status_code != 200:
                return None
            res = response.json()
            if not res or res['status'] == 0:
                return None
            return res
        except Exception as e:
            logging.error(str(e))
            return None

    def get_district_boundary(self, adcode):
        """ 返回三级地址（区）的边界（多边形）
        注意：有些行政区的边界包含多个多边形，例如北京市朝阳区
        :param adcode: 高德地图API支持的地址code
        :return: [[(x11,y11), (x12,y12), ...],  # 多边形1
                  [(x21,y21), (x22,y22), ...]]  # 多边形2 ...
        """
        url = "https://restapi.amap.com/v3/config/district?parameters"
        params = {
            'key': self._key,
            'keywords': adcode,
            'subdistrict': 0,
            'extensions': 'all',
            'output': 'JSON'
        }
        res = self._request(url, params)
        logging.info("Got district boundary from amap service.")
        return self._format_polygons(res['districts'][0]['polyline']) if res else None

    @staticmethod
    def _format_polygons(boundary_string):
        poly_list = boundary_string.split('|')
        poly_items = [list(map(lambda s: s.split(','), loc_str.split(';')))
                      for loc_str in poly_list]
        return [list(map(lambda item: (float(item[0]), float(item[1])), loc))
                for loc in poly_items]


logging.basicConfig(level=logging.INFO)
