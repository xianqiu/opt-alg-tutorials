import numpy as np


def binary_search(f, a, b):
    """
    Find a root of f(x) = 0 in the interval [a, b] using binary search.

    Parameters
    ----------
    f : function
        Function whose root we want to find.
    a : float
        Left endpoint of the interval.
    b : float
        Right endpoint of the interval.
    
    Returns
    -------
    float
        Root of f(x) = 0 in the interval [a, b].
    """
    while a < b:
        c = (a + b) / 2
        if np.isclose(f(c), 0):
            return c
        elif f(a) * f(c) < 0:
            return binary_search(f, a, c)
        elif f(b) * f(c) < 0:
            return binary_search(f, c, b)
        else:
            return None

    
if __name__ == '__main__':
    f = lambda x: x**2 - 2
    a, b = 0, 2
    print(binary_search(f, a, b))
