def count_inversions(a):
    s, count = sort_and_count(a)
    return count


def sort_and_count(x):
    if len(x) == 1:
        return x, 0
    k = len(x) // 2
    left, count_left = sort_and_count(x[0: k])
    right, count_right = sort_and_count(x[k:])
    # 把子问题的解拼接成原问题的解
    combined, count = merge_and_count(left, right)
    return combined, count + count_left + count_right


def merge_and_count(left, right):
    """ 把left和right合并且计算inversion的数量
    注意: left和right已经排好序
    """
    combined = []
    count = 0
    while len(left) and len(right):
        if left[0] > right[0]:  # 反序(左边的编号小于右边的编号是正序)
            combined.append(right.pop(0))
            count += len(left)
        else:  # 正序
            combined.append(left.pop(0))
    return combined + left + right, count


if __name__ == '__main__':
    print(count_inversions([1, 2, 3, 4, 5]))
    print(count_inversions([2, 4, 1, 3, 5, 6, 8, 9, 7]))
    print(count_inversions([3, 8, 4, 1, 2, 6, 7, 5, 9]))
    print(count_inversions([3, 6, 1, 2, 0, 5, 8, 4, 7]))
