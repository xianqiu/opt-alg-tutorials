def newton_method(f, f1, x0, epsilon=1e-6, max_iter=1000):
    """
    Newton's method to find the root of a function.

    Parameters
    ----------
    f : function
        The function to find the root of.
    f1 : function
        The derivative of the function f.
    x0 : float
        The initial guess.
    epsilon : float, optional
        The desired accuracy. The default is 1e-6.
    max_iter : int, optional
        The maximum number of iterations. The default is 1000.

    Returns
    -------
    float
        The root of the function.

    Raises
    ------
    ValueError
        If the algorithm does not converge.
    """
    x = x0
    for _ in range(max_iter):
        x_new = x - f(x) / f1(x)
        if abs(x_new - x) < epsilon:
            return x_new
        x = x_new
    raise ValueError("Newton's method did not converge")


if __name__ == '__main__':
    f = lambda x: x**2 - 2
    f1 = lambda x: 2 * x
    x0 = 1
    print(newton_method(f, f1, x0))