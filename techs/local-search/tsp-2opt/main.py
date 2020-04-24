from data import CityLocations
from tsp_2opt import TSP2opt
from gif_result import GifResult


if __name__ == '__main__':
    # 数据对象
    c = CityLocations()
    # 用2opt求解TSP问题
    tsp = TSP2opt(c.get_distance_matrix()).solve()
    tsp.print_result()
    # 计算过程保存为gif(可视化）
    # tours = tsp.get_tours()
    # GifResult(tours, c.locations).format()