import numpy as np


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


def strassen(A, B):
    n = A.shape[0]
    if n == 1:
        return A * B
    else:
        A11, A12, A21, A22 = A[:n//2, :n//2], A[:n//2, n//2:], A[n//2:, :n//2], A[n//2:, n//2:]
        B11, B12, B21, B22 = B[:n//2, :n//2], B[:n//2, n//2:], B[n//2:, :n//2], B[n//2:, n//2:]
        P1 = strassen(A11, B12 - B22)
        P2 = strassen(A11 + A12, B22) 
        P3 = strassen(A21 + A22, B11) 
        P4 = strassen(A22, B21 - B11) 
        P5 = strassen(A11 + A22, B11 + B22) 
        P6 = strassen(A12 - A22, B21 + B22) 
        P7 = strassen(A11 - A21, B11 + B12)
        C11 = P5 + P4 - P2 + P6
        C12 = P1 + P2
        C21 = P3 + P4
        C22 = P1 + P5 - P3 - P7
        return np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))


def test_simple_divide_and_conquer():
    for _ in range(10):
        for k in range(6):
            n = pow(2, k)
            A = np.random.randint(0, 10, (n, n))
            B = np.random.randint(0, 10, (n, n))
            assert np.allclose(simple_divide_and_conquer(A, B), A@B)
    print("[test_simple_divide_and_conquer] Passed.")


def test_strassen():
    for _ in range(10):
        for k in range(6):
            n = pow(2, k)
            A = np.random.randint(0, 10, (n, n))
            B = np.random.randint(0, 10, (n, n))
            assert np.allclose(strassen(A, B), A@B)
    print("[test_strassen] Passed.")


if __name__ == '__main__':
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(strassen(A, B))
