def valid_inn(value: str) -> bool:
    if not value.isdigit() or len(value) not in (10, 12):
        return False
    nums = [int(c) for c in value]
    def digit(weights):
        return sum(a * b for a, b in zip(nums, weights)) % 11 % 10
    if len(nums) == 10:
        return digit([2, 4, 10, 3, 5, 9, 4, 6, 8]) == nums[9]
    return (digit([7, 2, 4, 10, 3, 5, 9, 4, 6, 8]) == nums[10]
            and digit([3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]) == nums[11])
