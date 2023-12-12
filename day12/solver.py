from ast import literal_eval
from functools import lru_cache
from typing import List

from advent_of_code_solver import BaseSolver


def get_valid_arrangements(s: str, nums: List[int]) -> int:
    @lru_cache(None)
    def dp(i: int, j: int, group_length: int) -> int:
        """
        | Algorithm:
        | - Base case: if we reach the end of the string, we check if we have reached the end of the numbers
            and if the last group length is 0
        | - If the current character is a dot or a question mark, there are two options:
        |   - The current group length is equal to the current number in nums and nums has not reached the end,
            then we can start a new group
        |   - The current group length is 0, then we just skip the current character
        | - If the current character is a hash or a question mark, we can extend the current group length by 1
        :param i: The current index in the string
        :param j: The current index in the numbers
        :param group_length: The current group length
        :return: For the first i characters in the string, and the first j numbers, and the current group length,
            the number of valid arrangements
        """
        if i == len(s):
            # Check if we have reached the end of the numbers and if the last group length is 0
            return 1 if j == len(nums) and group_length == 0 else 0

        result = 0

        if s[i] == "." or s[i] == "?":
            if j < len(nums) and nums[j] == group_length:
                # Move to the next number and start a new group
                result += dp(i + 1, j + 1, 0)
            elif group_length == 0:
                # Simply skip the current character
                result += dp(i + 1, j, 0)

        if s[i] == "#" or s[i] == "?":
            # Extend the current group length by 1
            result += dp(i + 1, j, group_length + 1)

        return result

    # Add a dot at the end of the string so that we can check if the last group length is 0
    s += "."
    return dp(0, 0, 0)


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []
        for line in file.read().splitlines():
            s, nums = line.split()
            nums = literal_eval(f"[{nums}]")
            result.append((s, nums))

        return result

    def solve_part1(self):
        return sum(get_valid_arrangements(s, nums) for s, nums in self.input)

    def solve_part2(self):
        result = 0

        for s, nums in self.input:
            s, nums = "?".join([s] * 5), nums * 5
            result += get_valid_arrangements(s, nums)

        return result
