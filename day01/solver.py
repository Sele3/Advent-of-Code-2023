from advent_of_code_solver import BaseSolver

DIGIT_LETTERS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def get_first_and_last_digit(s: str) -> (int, int, int, int):
    """
    Returns the first and last digit of a string, as well as their indices.
    :return: A tuple of (first_digit, first_digit_index, last_digit, last_digit_index)
    """

    first, first_idx, last, last_idx = 0, float("inf"), 0, float("-inf")

    for idx, char in enumerate(s):
        if not char.isdigit():
            continue

        if first == 0:
            first = int(char)
            first_idx = idx

        last = int(char)
        last_idx = idx

    return first, first_idx, last, last_idx


def process_line(line: str) -> (int, int):
    """
    Process a line to find the first and last digit, including digits represented by letters.
    :return: A tuple of (first_digit, last_digit)
    """
    first, first_idx, last, last_idx = get_first_and_last_digit(line)

    for digit, letter in enumerate(DIGIT_LETTERS, start=1):
        idx1, idx2 = line.find(letter), line.rfind(letter)
        if idx1 == -1:
            continue

        if idx1 < first_idx:
            first, first_idx = digit, idx1
        if idx2 > last_idx:
            last, last_idx = digit, idx2

    return first, last


class Solver(BaseSolver):
    def parse_input(self, file):
        return file.read().splitlines()

    def solve_part1(self):
        result = 0

        for line in self.input:
            first, _, last, _ = get_first_and_last_digit(line)
            result += first * 10 + last

        return result

    def solve_part2(self):
        result = 0

        for line in self.input:
            first, last = process_line(line)
            result += first * 10 + last

        return result
