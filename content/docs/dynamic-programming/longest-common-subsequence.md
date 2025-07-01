---
weight: 330
title: "Longest Common Subsequence"
description: ""
icon: "article"
date: "2025-06-24T20:00:21+08:00"
lastmod: "2025-06-24T20:00:21+08:00"
draft: false
toc: true
katex: true
---

Consider two strings `s` and `s'`, if `s` contains all the characters of `s'` in the same order, then `s'` is called a **subsequence** of `s`. For example, `acdf` is a subsequence of `abcdeef`, but `acdf` is not a subsequence of `abccef`.

Given two strings `X` and `Y`, the **longest common subsequence** (LCS) problem is to find the longest subsequence which is common to both `X` and `Y`.

**Example**

* `X = ABCBDAB`
* `Y = BDCABA`

The longest common subsequence of `X` and `Y` is `BCBA`, of length 4.

We use **dynamic programming** to solve this problem. The first step is to define a subproblem, after that derive a recursive formula. Using this formula, we can compute the value of the subproblem. Finally, we construct the optimal solution from the computed values.

## Subproblem

Let `X` and `Y` be the input strings, and let `m` and `n` be the lengths of `X` and `Y` respectively. 

Given an index `i < m`, we define a subsequence `X[1 .. i]` as the first `i` elements of `X`. Similarly, given an index `j < n`, `Y[1 .. j]` contains the first `j` elements of `Y`.

Now we define the subproblem as follows:

Given `i, j`, find the length of the longest common subsequence of `X[1 .. i]` and `Y[1 .. j]`. For ease of description, the value is denote by `c[i, j]`. 

If we are able to find `c[i, j]` for all `i, j`, then the length of the longest common subsequence of `X` and `Y` is `c[m, n]`.

## Recursive Formula

We derive a recursive formula, by considering the last element of `X[0 .. i]` and `Y[0 .. j]`.

There are two cases:

1. If `X[i] = Y[j]`, then they must be in the longest common subsequence of `X[1 .. i]` and `Y[1 .. j]`. So `c[i, j] = c[i-1, j-1] + 1`.
2. If `X[i] != Y[j]`, then `X[i]` and `Y[j]` cannot be in the longest common subsequence of `X[1 .. i]` and `Y[1 .. j]`. So `c[i, j] = max(c[i-1, j], c[i, j-1])`.

Summarizing, for $1 \leq i \leq m$, $1 \leq j \leq n$, we have the following recursive formula:
{{<katex>}}
$$
c[i, j] = \begin{cases}
c[i-1, j-1] + 1 & \text{if } X[i-1] = Y[j-1] \\
\max(c[i-1, j], c[i, j-1]) & \text{if } X[i-1] \neq Y[j-1]
\end{cases}
$$
{{</katex>}}

**Initial Conditions**

In order to compute the values of `c[i,j]` w.r.t. the recursive formula, we need to know the initial conditions, that is `c[0, j]` and `c[i, 0]`. It is easy to see that `c[0, j] = 0` and `c[i, 0] = 0`.

## Implementation

We can use **bottom-up** or **top-down with memoization** to implement the dynamic programming algorithm. 

From my perspective, bottom-up is easier to implement. As it is not recursive, it is convenient to check the logic and see the intermediate results.

The following is a bottom-up implementation.

```python

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
```

## Solution

Note that the above implementation only returns the **length** of the longest common subsequence. In order to get the **subsequence**, we need to record the optimal solution chosen when computing `c[i, j]`.

We maintain a table `b[i, j]` to help us construct the optimal solution. Similar to the above discussion, we consider three cases:

1. If `X[i] = Y[j]`, then `c[i, j] = c[i - 1, j - 1] + 1`. Let `b[i, j] = 1`. 
2. If `X[i] != Y[j]` and `c[i-1, j] >= c[i, j-1]`, then `c[i, j] = c[i - 1, j]`. Let `b[i, j] = 2`.
3. If `X[i] != Y[j]` and `c[i-1, j] < c[i, j-1]`, then `c[i, j] = c[i, j - 1]`. Let `b[i, j] = 3`.

We modify the above implementation to return the length and the table `b` as below.

```python

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
```

The solution can be constructed by backtrack. 

```python

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
```
