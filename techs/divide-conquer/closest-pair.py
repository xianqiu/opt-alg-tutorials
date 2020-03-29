import math

import numpy as np


def get_dist(a, b):
    """ 计算两点之间的欧式距离
    """
    return math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2))


def search_closest_pair(points):
    """ 用枚举的方式寻找closest pair
    :param points: [(x1,y1), (x2,y2), ...]
    :return: closest pair
    """
    n = len(points)
    dist_min, i_min, j_min = math.inf, 0, 0
    for i in range(n-1):
        for j in range(i+1, n):
            d = get_dist(points[i], points[j])
            if d < dist_min:
                dist_min, i_min, j_min = d, i, j
    return points[i_min], points[j_min]


def get_sy(Py, Qx, d):
    """ 根据Py计算Sy.
    :param Py: P按y轴排序的结果
    :param Qx: P在x=x0处被切分成Q和R. Qx是Q按x轴排序的结果
    :param d: delta
    :return: S
    """
    x0 = Qx[-1][0]  # Q最右边点的x坐标值
    return [p for p in Py if p[0] - x0 < d]


def closest_pair_of_sy(Sy):
    """ 计算集合Sy的closest pair
    """
    n = len(Sy)
    if n <= 1:
        return None, None
    dist_min, i_min, j_min = math.inf, 0, 0
    for i in range(n-1):
        for j in range(i + 1, i + 16):
            if j == len(Sy):
                break
            d = get_dist(Sy[i], Sy[j])
            if d < dist_min:
                dist_min, i_min, j_min = d, i, j
    return Sy[i_min], Sy[j_min]


def combine_results_of_sub_problems(Py, Qx, q0, q1, r0, r1):
    """
    :param Py: P按y轴排序的结果
    :param Qx: P在x=x0处被切分成Q和R. Qx是Q按x轴排序的结果
    :param q0: (q0, q1)是Q中的closest pair
    :param q1: 参考q0
    :param r0: (r0, r1)是R中的closest pair
    :param r1: 参考r0
    :return: closest pair in P
    """
    # 计算Sy
    d = min(get_dist(q0, q1), get_dist(r0, r1))
    Sy = get_sy(Py, Qx, d)
    # 检查是否存在距离更小的pair
    s1, s2 = closest_pair_of_sy(Sy)
    if s1 and s2 and get_dist(s1, s2) < d:
        return s1, s2
    elif get_dist(q0, q1) < get_dist(r0, r1):
        return q0, q1
    else:
        return r0, r1


def closest_pair_xy(Px, Py):
    """ 计算closest pair
    :param Px: 把points按x轴升序排列
    :param Py: 把points按y轴升序排列
    :return: point1, point2
    """
    if len(Px) <= 3:
        return search_closest_pair(Px)
    # 构造子问题的输入: Qx, Rx, Qy, Ry
    k = len(Px) // 2
    Q, R = Px[0: k], Px[k:]
    Qx, Qy = sorted(Q, key=lambda x: x[0]), sorted(Q, key=lambda x: x[1])
    Rx, Ry = sorted(R, key=lambda x: x[0]), sorted(R, key=lambda x: x[1])
    # 求解子问题
    q0, q1 = closest_pair_xy(Qx, Qy)
    r0, r1 = closest_pair_xy(Rx, Ry)
    # 合并子问题的解
    return combine_results_of_sub_problems(Py, Qx, q0, q1, r0, r1)


def closest_pair(points):
    """ 计算二维点集中的closest pair.
    :param points: P = [(x1,y1), (x2,y2), ..., (xn, yn)]
    :return: 两个距离最近的点
    """

    # 把P按x轴和y轴分别进行排序, 得到Px和Py
    # 注意: P, Px, Py 三个集合是相同的(仅仅排序不同)
    Px = sorted(points, key=lambda item: item[0])
    Py = sorted(points, key=lambda item: item[1])
    return closest_pair_xy(Px, Py)


def generate_test_points(point_num):
    p = set({})
    for i in range(point_num):
        p.add(tuple(np.random.randint(1, 1000, (1, 2))[0]))
    return list(p)


if __name__ == '__main__':
    points = generate_test_points(100)
    p1, p2 = closest_pair(points)
    print(p1, p2, get_dist(p1, p2))







