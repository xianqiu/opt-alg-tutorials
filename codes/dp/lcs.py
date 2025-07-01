def lcs_length(X, Y):
    """ Returns the **length** of the LCS of X and Y.
    """
    m = len(X)
    n = len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[-1] == Y[-1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    return c[m][n]


def lcs_length_b(X, Y):
    """ Returns the length of the LCS of X and Y and the b table.
    The b table helps to print the LCS.
    """
    m = len(X)
    n = len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 2
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 3
    return c[m][n], b


def get_lcs(b, X, i, j, res):
    """ Returns the LCS of X and Y given the b table in a recursive manner.
    The result is stored in res. The function is called with i = len(X) and j = len(Y).
    """
    if i == 0 or j == 0:
        return
    if b[i][j] == 1:
        # X[i - 1] == Y[j - 1] is in the optimal solution
        get_lcs(b, X, i - 1, j - 1, res)   
        res.append(X[i - 1])
    elif b[i][j] == 2:
        # c[i, j] = c[i - 1, j]
        get_lcs(b, X, i - 1, j, res)
    else:
        # c[i, j] = c[i, j - 1]
        get_lcs(b, X, i, j - 1, res)


def LCS(X, Y):
    """ Returns the LCS of X and Y.
    """
    _, b = lcs_length_b(X, Y)
    res = []
    get_lcs(b, X, len(X), len(Y), res)
    return "".join(res)


if __name__ == '__main__':
    X = "ABCBDAB"
    Y = "BDCABA"
    print(LCS(X, Y))