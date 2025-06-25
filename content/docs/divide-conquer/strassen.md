---
weight: 120
title: "Matrix Multiplication"
description: ""
icon: "article"
date: "2025-06-24T19:18:42+08:00"
lastmod: "2025-06-24T19:18:42+08:00"
draft: false
toc: true
katex: true
---

Consider two square matrices $A=(a_{ij})$ and $B=(b_{ij})$ of size $n \times n$, where $n$ is a power of 2. The product $C=A \times B$ is defined as

$$
c_{ij} = \sum_{k=1}^n a_{ik} b_{kj},
$$

where $c_{ij}$ is the element of $C$ in the $i$-th row and $j$-th column.

As $c_{ij}$ can be computed in $O(n)$, and $i, j$ takes values from $1$ to $n$, the computation time is $O(n^3)$.

## Divide and conquer

Let us consider a simple divide and qonquer algorithm. The idea is to divide $A$, $B$, and $C$ into $\frac{n}{2}\times \frac{n}{2}$ matrices in a recursive way, i.e. 

{{<katex>}}
$$
A = \begin{bmatrix}
A_{11} & A_{12} \\
A_{21} & A_{22}
\end{bmatrix}
, \quad
B = \begin{bmatrix}
B_{11} & B_{12} \\
B_{21} & B_{22}
\end{bmatrix}
, \quad
C = \begin{bmatrix}
C_{11} & C_{12} \\
C_{21} & C_{22}
\end{bmatrix}
$$
{{</katex>}}

Then, compute the following products:

{{<katex>}}
$$
\begin{aligned}
C_{11}  &= A_{11} \times B_{11} + A_{12} \times B_{21} \\
C_{12}  &= A_{11} \times B_{12} + A_{12} \times B_{22} \\
C_{21}  &= A_{21} \times B_{11} + A_{22} \times B_{21} \\
C_{22}  &= A_{21} \times B_{12} + A_{22} \times B_{22} \\
\end{aligned}
$$
{{</katex>}}

The algorithm can be implemented as below.

```python

def simple_divide_and_conquer(A, B):
    n = A.shape[0]
    if n == 1:
        return A * B
    else:
        A11, A12, A21, A22 = A[:n//2, :n//2], A[:n//2, n//2:], A[n//2:, :n//2], A[n//2:, n//2:]
        B11, B12, B21, B22 = B[:n//2, :n//2], B[:n//2, n//2:], B[n//2:, :n//2], B[n//2:, n//2:]
        C11 = simple_divide_and_conquer(A11, B11) + simple_divide_and_conquer(A12, B21)
        C12 = simple_divide_and_conquer(A11, B12) + simple_divide_and_conquer(A12, B22)
        C21 = simple_divide_and_conquer(A21, B11) + simple_divide_and_conquer(A22, B21)
        C22 = simple_divide_and_conquer(A21, B12) + simple_divide_and_conquer(A22, B22)
        return np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
```
Let $T(n)$ be the running time of the algorithm. 

As described above, each recursive call multiplies two $(\frac{n}{2}\times \frac{n}{2})$ matrices, and there are $8$ such calls, the corresponding time is $8T(n/2)$. 

Besides, each of the matrices contains $n^2/4$ elements, so each of the four matrix additions takes $\Theta(n^2)$ time. Therefore,

$$T(n) = 8T(n/2) + O(n^2).$$

According to the **master theorem**, the running time of the algorithm is 

$$T(n) = O(n^{\log_2 8}) = O(n^3),$$

which means it is not better than the direct method by definition. 

## Strassen's algorithm

Strassen's algorithm is also a divide and conquer algorithm, which computes the product of two $n\times n$ matrices in $O(n^{\log_2 7}) = O(n^{2.81})$ time. 

The idea is to use the following 7 multiplications of $(\frac{n}{2}\times \frac{n}{2})$ matrices instead of 8 multiplications of $(\frac{n}{2}\times \frac{n}{2})$ matrices in the simple divide and conquer algorithm.




