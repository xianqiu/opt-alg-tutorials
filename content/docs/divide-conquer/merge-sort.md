---
weight: 110
title: "Merge Sort"
description: ""
icon: "article"
date: "2025-06-24T19:05:11+08:00"
lastmod: "2025-06-24T19:05:11+08:00"
draft: false
toc: true
---

This is to demonstrate the **divide and conquer** algorithm for the sorting problem. 

## Sorting

The sorting problem is defined as below: Given `n` numbers, sort them in ascending order. For example, given `5, 4, 11, 2, 10, 8, 4`, the sorted result is `2, 4, 4, 5, 8, 10, 11`.

## Algorithm

The divide and conquer algorithm for the sorting problem is called **merge sort**.

The basic idea is as follows:
1. Divide the `n` numbers into two subsequences of `n/2` numbers each (if `n = 1` then return).
2. Conquer the two subsequences **recursively** using the divide and conquer algorithm itself.
3. Merge the two sorted subsequences to produce the sorted result.

## Example

**Input** `[5, 4, 11, 2, 10, 8, 4]`

**Divide**

1. The list `[5, 4, 11, 2, 10, 8, 4]` is divided into sub-lists `[5, 4, 11, 2]` and `[10, 8, 4]`.
2. These sub-lists are further divided:
    * `[5, 4, 11, 2]` becomes `[5, 4]` and `[11, 2]`.
    *  `[10, 8, 4]` becomes `[10, 8]` and `[4]`.
3. This continues until each sub-list has only one element: `[5], [4], [11], [2], [10], [8], [4]`.

**Conquer**

1. Merge pairs of sub-lists:
    * `[5]` and `[4]` merge to `[4, 5]`.
    * `[11]` and `[2]` merge to `[2, 11]`.
    * `[10]` and `[8]` merge to `[8, 10]`.
    * `[4]` remains `[4]`.
2. Merge sorted sub-arrays:
    * `[4, 5]` and `[2, 11]` merge to `[2, 4, 5, 11]`.
    * `[8, 10]` and `[4]` merge to `[4, 8, 10]`.
3. Final merge:
    * `[2, 4, 5, 11]` and `[4, 8, 10]` merge to `[2, 4, 4, 5, 8, 10, 11]`.

## Code

Define two functions:
* `merge_sort` to sort the list (divide).
* `merge` to merge two sorted sub-lists (conquer).

```python

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

```python

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result
```

Run the code as below and yield the sorted result.

```python

if __name__ == '__main__':
    arr = [5, 4, 11, 2, 10, 8, 4]
    print(merge_sort(arr))
```