def subset_sum_dfs(numbers, target):

    def dfs(subset, index):
        current_sum = sum(subset)
        if current_sum == target:
            return subset
        if current_sum > target:
            return None
        if index == len(numbers):
            return None
        return dfs(subset + [numbers[index]], index + 1) or dfs(subset, index + 1)
    
    return dfs([], 0)


if __name__ == "__main__":
    numbers = [3, 8, 10, 6, 7]
    target = 15
    print(subset_sum_dfs(numbers, target))