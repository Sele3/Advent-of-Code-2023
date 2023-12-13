from itertools import combinations
from typing import List

from advent_of_code_solver import BaseSolver

SYMBOLS = {
    ".": 0,
    "#": 1,
}


def get_palindrome_index(nums: List[int], ignore_idx: int = -1) -> int:
    """
    Get the index of the reflection point that forms a palindrome
    :param nums: The list of numbers
    :param ignore_idx: Optional parameter which is only used for part 2 to ignore the original index
    """
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            continue

        left, right = i - 2, i + 1
        while left >= 0 and right < len(nums) and nums[left] == nums[right]:
            left -= 1
            right += 1

        if (left == -1 or right == len(nums)) and i != ignore_idx:
            return i

    return -1


def convert_grid_to_nums(grid: List[str]) -> List[int]:
    """
    Convert the list of strings to a list of numbers
    """
    result = []
    for row in grid:
        row_num = 0
        for symbol in row:
            row_num = (row_num << 1) | SYMBOLS[symbol]
        result.append(row_num)

    return result


def summarize_pattern_notes(grid: List[str]) -> int:
    """
    Part 1, summarize a single pattern note
    """
    row_nums = convert_grid_to_nums(grid)

    if (idx := get_palindrome_index(row_nums)) != -1:
        return idx * 100

    col_nums = convert_grid_to_nums(list(zip(*grid)))
    return get_palindrome_index(col_nums)


def summarize_smudged_pattern_notes(grid: List[str]) -> int:
    """
    Part 2, summarize a single smudged pattern note
    """

    def get_new_palindrome_index(nums: List[int]) -> int:
        """
        Get the index of the new reflection point that forms a palindrome, when a single character is flipped
        """
        old_idx = get_palindrome_index(nums)

        # Iterate through all possible pairs of indices
        for i, j in combinations(range(len(nums)), 2):
            # Check if the pair of indices has an even distance and differ by only 1 bit
            if not ((j - i + 1) % 2 == 0 and (nums[i] ^ nums[j]).bit_count() == 1):
                continue

            # Temporarily set the value of the first index to the value of the second index
            temp = nums[i]
            nums[i] = nums[j]
            if (idx := get_palindrome_index(nums, old_idx)) != -1:
                return idx

            # Set the value of the first index back to the original value if no palindrome is found
            nums[i] = temp

        return -1

    row_nums = convert_grid_to_nums(grid)
    if (idx := get_new_palindrome_index(row_nums)) != -1:
        return idx * 100

    col_nums = convert_grid_to_nums(list(zip(*grid)))
    return get_new_palindrome_index(col_nums)


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []
        for grids in file.read().split("\n\n"):
            result.append(grids.splitlines())
        return result

    def solve_part1(self):
        return sum(summarize_pattern_notes(grid) for grid in self.input)

    def solve_part2(self):
        return sum(summarize_smudged_pattern_notes(grid) for grid in self.input)
