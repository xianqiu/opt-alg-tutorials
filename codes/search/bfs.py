from collections import deque


def subset_sum_bfs(numbers, target):
    queue = deque()
    queue.append(([], 0, 0)) # (current subset, current sum, start index)
    while queue:
        subset, current_sum, start = queue.popleft()
        if current_sum == target:
            return subset
        if current_sum > target:
            continue
        for i in range(start, len(numbers)):
            new_subset = subset + [numbers[i]]
            new_sum = current_sum + numbers[i]
            queue.append((new_subset, new_sum, i + 1))
    return None


if __name__ == "__main__":
    numbers = [3, 8, 10, 6, 7]
    target = 15
    print(subset_sum_bfs(numbers, target))