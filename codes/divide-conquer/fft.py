import numpy as np


def FFT(v):
    """ Fast Fourier Transform.
    """
    n = len(v)
    if n == 1:
        return v
    v_even = FFT(v[0:n:2])
    v_odd = FFT(v[1:n:2])
    u = [np.e ** (-2 * np.pi * complex(0, 1) * j / n) for j in range(n//2)]
    part1 = [v_even[i] + u[i]*v_odd[i] for i in range(n//2)]
    part2 = [v_even[i] - u[i]*v_odd[i] for i in range(n//2)]
    return part1 + part2


def test_fft():
    for _ in range(100):
        for k in range(10):
            n = pow(2, k)
            v = np.random.randint(0, 100, n)
            assert np.allclose(FFT(v), np.fft.fft(v))
    print('[FFT] test passed.')


def iFFT(v):
    """ Inverse of the Fast Fourier Transform.
    """
    n = len(v)
    u = FFT(v)
    x = [i/n for i in u]  # u divided by n
    # Reverse the last n-1 elements
    y = x[1:]
    y.reverse()  
    return x[0:1] + y


if __name__ == '__main__':
    v = [1, 2, 3, 4, 5, 6, 7, 8]
    print(FFT(v))
    

    