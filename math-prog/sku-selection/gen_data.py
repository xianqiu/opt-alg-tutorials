import numpy as np


def gen_p(m, n):
    """
    :param m: 品牌的个数
    :param n: 商品的个数是[n, 2*n]之间的随机数
    :return: p[i][j] 品牌i中商品j的预期收益. 数值范围在100-200之间
    """
    ni = np.random.randint(n, 2*n, (m, ))
    p = [None] * m
    for i in range(m):
        p[i] = np.random.randint(100, 200, (ni[i],)).tolist()
    return p


def gen_c(p):
    """
    :return: c[i][j] 品牌i中商品j的营销成本. 数值范围在10-50之间
    """
    c = [None] * len(p)
    for i in range(len(p)):
        c[i] = np.random.randint(10, 50, (len(p[i], ))).tolist()
    return c


def gen_b(p):
    """
    :return: b[i] 选择品牌商i的商品数量限制
    """
    b = [0] * len(p)
    for i in range(len(p)):
        ni = len(p[i])
        b[i] = np.random.randint(ni//2, ni-1)
    return b


def gen_d(c, b):
    c_mean = []
    for i in range(len(c)):
        c_mean.append(np.mean(c[i]))
    return sum(c_mean) * np.mean(b)


def gen_data(m, n):
    p = gen_p(m, n)
    c = gen_c(p)
    b = gen_b(p)
    d = gen_d(c, b)

    with open('data.py', 'w') as f:
        lines = ['[' + ', '.join(map(lambda x: ("%d" % x), line)) + ']' for line in p]
        lines = 'p = [' + ',\n'.join(lines) + ']\n\n'
        f.writelines(lines)

        lines = ['[' + ', '.join(map(lambda x: ("%d" % x), line)) + ']' for line in c]
        lines = 'c = [' + ',\n'.join(lines) + ']\n\n'
        f.writelines(lines)

        line = 'b = [' + ', '.join(map(lambda x: ("%d" % x), b)) + ']\n\n'
        f.writelines(line)

        line = 'd = %d\n\n' % d
        f.writelines(line)

    print(">>> A random instance is generated.")


if __name__ == '__main__':
    gen_data(10, 50)
