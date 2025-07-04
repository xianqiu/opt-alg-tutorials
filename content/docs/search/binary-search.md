---
weight: 240
title: "Binary Search"
description: ""
icon: "article"
date: "2025-07-03T14:07:03+08:00"
lastmod: "2025-07-03T14:07:03+08:00"
draft: false
toc: true
katex: true
---

Binary search is an efficient algorithm for finding a target value from a sorted list of numbers. It is a **[divide and conquer algorithm](docs/divide-conquer)**, which repeatedly divides the search interval in half until the target value is found or the interval is empty.

To illustrate this algorithm, we consider the following example.

## Root of Equation

Consider an equation $f(x) = 0$, where $f(x)$ is a continuous function, and there is an interval $[a, b]$ such that $f(a) \times f(b) < 0$. We want to find a root of $f(x)$ in the interval $[a, b]$.

The binary search algorithm works as follows:

1. Find the midpoint $c$ of $[a, b]$. If $f(c) = 0$, then $c$ is a root. 
2. If $f(c) \neq 0$, then we have $f(a) \times f(c) < 0$ or $f(b) \times f(c) < 0$. We then replace $a$ or $b$ with $c$, depending on which of the two inequalities is true. 
3. Repeat this process until we find a root or the interval is empty.

## Code

The algorithm is implemented as below.

```python
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
```

**Usage**

For example, we may use it to find the root of $f(x) = x^2 - 2$ in the interval $[0, 2]$.

```python

if __name__ == '__main__':
    f = lambda x: x**2 - 2
    a, b = 0, 2
    print(binary_search(f, a, b))
```