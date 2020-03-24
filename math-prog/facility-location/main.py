from benders_proc import BendersProc
from gen_data import f, C


if __name__ == '__main__':
    bp = BendersProc(f, C)
    bp.solve()
    bp.print_info()

