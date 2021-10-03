import numpy as np


def fft(v):
    """ 快速傅立叶变换
    注意：输入向量 v 的长度是2的幂次方。
    :param v: array like
    :return: array like（复向量）
    """
    n = len(v)
    if n == 1:
        return v

    v_even = [v[i] for i in range(0, n, 2)]
    v_odd = [v[i] for i in range(1, n, 2)]
    q1 = fft(v_even)
    q2 = fft(v_odd)
    s = [np.e ** (-2 * np.pi * complex(0, 1) * j / n) for j in range(n//2)]
    part1 = (np.array(q1) + np.array(q2) * s).tolist()
    part2 = (np.array(q1) - np.array(q2) * s).tolist()

    return part1 + part2


def ifft(v):
    """
    傅立叶变换的逆变换
    注意：输入向量 v 的长度是2的幂次方。
    :param v: array like
    :return: array like（复向量）
    """
    n = len(v)
    u = fft(v)
    # u 除以 n
    x = [i/n for i in u]
    # 对后n-1个元素逆序排列
    y = x[1:]
    y.reverse()
    return x[0:1] + y


if __name__ == '__main__':

    def test(n):
        v = np.random.random(n)
        u = fft(v)  # 傅立叶变换
        inv = ifft(u)  # 逆变换（inv = v）
        print("==== Fast Fourier Transform ====")
        print(">> input:", np.round(v, 2))
        print(">> result:", np.round(u, 2))
        print("==== Inverse Fourier Transform ====")
        print(">> inverse:", np.round(inv,2))

    test(n=8)
