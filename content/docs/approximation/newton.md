---
weight: 450
title: "Newton's Method"
description: ""
icon: "article"
date: "2025-06-24T20:05:04+08:00"
lastmod: "2025-06-24T20:05:04+08:00"
draft: false
toc: true
katex: true
---

Newton's method is a root-finding algorithm that uses the iterative process of repeatedly guessing and checking values until a solution is found. 

## Problem

Given a continous and differentiable function $f(x)$, find the root of $f(x)$, i.e., find $x$ such that $f(x) = 0$.

## Algorithm

The basic idea behind Newton's method is to approximate the root of a function by using a linear approximation to the function. 

We use the first order **Taylor expansion** of $f(x)$ at a point $x_k$ to approximate $f(x)$:

$$
f(x) \approx f(x_k) + f'(x_k)(x-x_k)
$$

where $x_k$ is the point we guess at step $k$. 

Now consider $x_{k+1}$ and substitute it into the above formula:
$$
f(x_{k+1}) \approx f(x_k) + f'(x_k)(x_{k+1}-x_k)
$$

We expect $f(x_{k+1}) = 0$ (or close to 0), then $x_{k+1}$ is the root (or is better than $x_k$).

Hence,
$$
f(x_k) + f'(x_k)(x_{k+1}-x_k) = 0
$$

We get the iterative formula:
$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$

## Code

```python

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
```

For example, we can use Newton's method to find the root of $f(x) = x^2 - 2$. The derivative of $f(x)$ is $f'(x) = 2x$. The initial guess is $x_0 = 1$.

```python

if __name__ == '__main__':
    f = lambda x: x**2 - 2
    f1 = lambda x: 2 * x
    x0 = 1
    print(newton_method(f, f1, x0))
```
