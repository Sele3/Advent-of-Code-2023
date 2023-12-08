from collections import Counter
from dataclasses import dataclass, field
from typing import List

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SORTED_HAND_STRENGTHS = [
    [1, 1, 1, 1, 1],  # High card
    [1, 1, 1, 2],  # One pair
    [1, 2, 2],  # Two pairs
    [1, 1, 3],  # Three of a kind
    [2, 3],  # Full house
    [1, 4],  # Four of a kind
    [5],  # Five of a kind
]


@dataclass
class Card:
    """
    Represents a single card. The rank is a single character from 2 to A.
    """

    rank: str

    def __lt__(self, other):
        return RANKS.index(self.rank) < RANKS.index(other.rank)

    def __eq__(self, other):
        return self.rank == other.rank

    def __hash__(self):
        return hash(self.rank)


@dataclass
class WildCard(Card):
    """
    A subclass of Card that replaces "J" with a Joker wildcard.
    """

    def __lt__(self, other):
        if self.rank == "J":
            return True
        if other.rank == "J":
            return False
        return super().__lt__(other)

    def __hash__(self):
        return super().__hash__()


def calculate_strength(cards: List[Card]) -> int:
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

    cards: List[Card]
    strength: int = field(init=False)

    def __post_init__(self):
        self.strength = self._calculate_strength()

    def _calculate_strength(self) -> int:
        return calculate_strength(self.cards)

    def __lt__(self, other):
        if self.strength != other.strength:
            return self.strength < other.strength

        for self_card, other_card in zip(self.cards, other.cards):
            if self_card != other_card:
                return self_card < other_card


@dataclass
class WildCardHand(CardHand):
    """
    A subclass of CardHand that replaces all cards with WildCards.
    """

    def __post_init__(self):
        self.cards = [WildCard(card.rank) for card in self.cards]
        super().__post_init__()

    def _calculate_strength(self) -> int:
        """
        Calculate the strength of the hand, but replace all Jokers with the most common card if there are 1-4 Jokers.
        """
        counter = Counter(self.cards)

        if 1 <= counter[Card("J")] <= 4:
            joker_count = counter.pop(Card("J"))
            most_common = counter.most_common(1)[0][0]
            counter[most_common] += joker_count

        wildcards = list(counter.elements())
        return calculate_strength(wildcards)


@dataclass
class CamelCard:
    """
    Represents a Camel Card. A Camel Card is a CardHand with a bid.
    """

    hand: CardHand
    bid: int

    def __lt__(self, other):
        return self.hand < other.hand
