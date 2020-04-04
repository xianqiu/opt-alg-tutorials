import numpy as np


def longest_common_subsequence(x, y):
    """ 根据递归式计算最长公共子序列
    """
    m, n = len(x), len(y)
    # 把x,y中字符的下标向右移一位(方便计算)
    x1 = ' ' + x
    y1 = ' ' + y
    # c[m][n]为最大公共子序列的长度
    c = np.zeros((m+1, n+1))  # 初始化c
    # 记录下标改变的路径(用字符串表示)
    b = np.zeros((m+1, n+1)).tolist()
    for i in range(1, m+1):
        for j in range(1, n+1):
            if x1[i] == y1[j]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = 'lu'  # go left up
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = 'u'  # go up
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = 'l'  # go left
    return get_common_subsequence(x1, y1, b)


def get_common_subsequence(x1, y1, b):
    """ 根据b还原最长公共子序列
    """
    i, j = len(x1) - 1, len(y1) - 1
    res = []
    while i and j:
        if x1[i] == y1[j]:
            res.insert(0, x1[i])
        if b[i][j] == 'lu':  # go left up
            i -= 1
            j -= 1
        elif b[i][j] == 'l':  # go left
            j -= 1
        elif b[i][j] == 'u':  # go up
            i -= 1
    return ''.join(res)


if __name__ == '__main__':
    lcs = longest_common_subsequence('ABCBDAB', 'BDCABA')
    print(lcs)
