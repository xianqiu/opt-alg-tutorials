from model import TransportModel


if __name__ == '__main__':
    # 供给量
    a = [100, 200, 300]
    # 需求量
    d = [120, 60, 270, 150]
    # 单位运输成本矩阵
    C = [
        [350, 200, 300, 250],
        [220, 330, 300, 270],
        [215, 230, 290, 240]
    ]
    tm = TransportModel(a, d, C)
    tm.solve()
    tm.print_result()
