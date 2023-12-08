from typing import List

from advent_of_code_solver import BaseSolver

from .utils import CamelCard, CardHand, WildCardHand


def get_total_winnings(cards: List[CamelCard]) -> int:
    sorted_cards = sorted(cards)
    return sum(rank * card.bid for rank, card in enumerate(sorted_cards, start=1))


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []

        for line in file.read().splitlines():
            cards, bid = line.split(" ")
            hand = CardHand(cards)
            result.append(CamelCard(hand, int(bid)))

        return result

    def solve_part1(self):
        return get_total_winnings(self.input)

    def solve_part2(self):
        camel_wildcards = [
            CamelCard(WildCardHand(card.hand.cards), card.bid) for card in self.input
        ]
        return get_total_winnings(camel_wildcards)
