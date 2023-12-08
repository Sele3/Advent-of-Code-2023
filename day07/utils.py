from collections import Counter
from dataclasses import dataclass, field
from typing import ClassVar, Tuple

SORTED_HAND_STRENGTHS = [
    [1, 1, 1, 1, 1],  # High card
    [1, 1, 1, 2],  # One pair
    [1, 2, 2],  # Two pairs
    [1, 1, 3],  # Three of a kind
    [2, 3],  # Full house
    [1, 4],  # Four of a kind
    [5],  # Five of a kind
]


def calculate_strength(cards: str) -> int:
    """
    Calculate the strength of a hand of cards. The strength is based on the Camel Card rules.
    """
    values = sorted(Counter(cards).values())
    return SORTED_HAND_STRENGTHS.index(values)


@dataclass
class CardHand:
    """
    Represents a hand of cards.
    """

    cards: str

    # The ordering of the cards, from lowest to highest.
    ordering: ClassVar[str] = field(init=False, default="23456789TJQKA")

    # Helper attributes
    strength: int = field(init=False)
    ranks: Tuple[int, ...] = field(init=False)

    def __post_init__(self):
        self.strength = self._calculate_strength()
        self.ranks = tuple(self.ordering.index(card) for card in self.cards)

    def _calculate_strength(self) -> int:
        return calculate_strength(self.cards)

    def __lt__(self, other):
        return (
            self.strength < other.strength
            if self.strength != other.strength
            else self.ranks < other.ranks
        )


@dataclass
class WildCardHand(CardHand):
    """
    A subclass of CardHand that can contain Jokers. The ordering of the cards is changed to make Jokers the lowest card.
    """

    ordering: ClassVar[str] = field(init=False, default="J23456789TQKA")

    def _calculate_strength(self) -> int:
        """
        Calculate the strength of the hand, but replace all Jokers with the most common card if there are 1-4 Jokers.
        """
        counter = Counter(self.cards)

        if 1 <= counter["J"] <= 4:
            joker_count = counter.pop("J")
            most_common = counter.most_common(1)[0][0]
            counter[most_common] += joker_count

        cards = "".join(counter.elements())
        return calculate_strength(cards)


@dataclass
class CamelCard:
    """
    Represents a Camel Card. A Camel Card is a CardHand with a bid.
    """

    hand: CardHand
    bid: int

    def __lt__(self, other):
        return self.hand < other.hand
