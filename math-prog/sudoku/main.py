from model import SudokuModel
from data import a


if __name__ == '__main__':
    sm = SudokuModel(a)
    sm.solve()
    sm.print_result()
