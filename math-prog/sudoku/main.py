import numpy as np

# -----------------
# Sudoku instance #
# -----------------

a = np.zeros((3, 3, 3, 3, 9))

# 区块[0][0]
a[0][0][0][1][1] = 1  # 位置1的值为1代表数字2
a[0][0][2][0][0] = 1
# 区块[0][1]
a[0][1][0][1][2] = 1
# 区块[0][2]
a[0][2][0][1][8] = 1
a[0][2][2][0][6] = 1
# 区块[1][0]
a[1][0][1][0][4] = 1
a[1][0][2][2][6] = 1
# 区块[1][1]
a[1][1][0][1][3] = 1
a[1][1][1][1][5] = 1
# 区块[1][2]
a[1][2][0][1][5] = 1
a[1][2][0][2][1] = 1
# 区块[2][0]
a[2][0][0][2][8] = 1
a[2][0][1][1][3] = 1
# 区块[2][1]
a[2][1][0][0][6] = 1
a[2][1][0][2][0] = 1
a[2][1][2][0][4] = 1
# 区块[2][2]
a[2][2][1][1][1] = 1


if __name__ == '__main__':

    from model import SudokuModel
    sm = SudokuModel(a)
    sm.solve()
    sm.print_result()
