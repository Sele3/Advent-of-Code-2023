import re
from typing import List

from advent_of_code_solver import BaseSolver

from .utils import ScratchCard


def get_total_scratchcards(scratchcards: List[ScratchCard]) -> int:
    """
    Calculates the total number of scratchcards that have been won.

    | Intuition:
    | - The number of scratchcards doubles at each iteration.
    | - Let dp[i] be the number of scratchcards to subtract from the total at the i-th iteration.
    | - Let curr be the number of scratchcards at the i-th iteration.
    | - We can add curr to dp[i + matches + 1] to get the number of scratchcards to subtract
        at the (i + matches + 1)-th iteration.
    |
    | Optimizations:
    | - We can use a circular buffer of size (n + 1) to store the dp values,
        since we at most need add curr to dp[i + n + 1].
    """
    n = len(scratchcards[0].winning_numbers) + 1
    dp = [0] * n
    total, curr = 0, 1

    for idx, card in enumerate(scratchcards):
        idx %= n
        curr -= dp[idx]
        dp[idx] = 0
        total += curr

        matches = card.get_number_of_matches()
        dp[(idx + matches + 1) % n] += curr
        curr *= 2

    return total


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []

        for line in file.read().splitlines():
            match = re.match(r"Card\s+\d+: ([\d|\s]+) \| ([\d|\s]+)", line)
            before_pipe, after_pipe = match.groups()

            winning_numbers = list(map(int, before_pipe.split()))
            card_numbers = list(map(int, after_pipe.split()))

            result.append(ScratchCard(winning_numbers, card_numbers))

        return result

    def solve_part1(self):
        scratchcards: List[ScratchCard] = self.input
        return sum(card.points for card in scratchcards)

    def solve_part2(self):
        scratchcards: List[ScratchCard] = self.input
        return get_total_scratchcards(scratchcards)
