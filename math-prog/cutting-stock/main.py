from cg_proc import CGProc
from gen_data import s, d, L
from rouding_proc import RoundingProc


if __name__ == '__main__':
    # 1. 用列生成模型求解原问题的LP松弛问题
    c = CGProc(s, d, L)
    c.solve()
    c.print_info()
    # 2. 得到松弛问题的解
    A = c.get_solution_matrix()
    x = c.get_solution_x()
    # 3. 对分数解向下取整,然后用直观的方式满足需求,得到最终的解
    r = RoundingProc(A, x, s, d, L)
    r.solve()
    r.print_info()
