from data import p, c, b, d  # instance data
from dw_proc import DWProc


if __name__ == '__main__':
    dw = DWProc(p, c, d, b)
    dw.solve()
    dw.print_info()
