import re

from advent_of_code_solver import BaseSolver

DIGIT_LETTERS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def get_calibration_value(line: str) -> int:
    """
    Get the calibration value, which is the combination of the first and last digit of the line.
    """
    digits = re.findall(r"\d", line)
    return int(digits[0] + digits[-1])


def replace_digit_letters(line: str) -> str:
    """
    Replace digit letters with their corresponding digits.
    """
    for digit, letter in enumerate(DIGIT_LETTERS, start=1):
        line = line.replace(letter, f"{letter}{digit}{letter}")

    return line


class Solver(BaseSolver):
    def parse_input(self, file):
        return file.read().splitlines()

    def solve_part1(self):
        return sum(get_calibration_value(line) for line in self.input)

    def solve_part2(self):
        return sum(
            get_calibration_value(replace_digit_letters(line)) for line in self.input
        )
