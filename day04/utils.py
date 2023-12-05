from dataclasses import dataclass, field
from typing import List


@dataclass
class ScratchCard:
    winning_numbers: List[int]
    card_numbers: List[int]

    # Helper attributes
    all_numbers: List[bool] = field(
        init=False, default_factory=lambda: [False] * 100
    )  # Stores all numbers on the card

    # Solution-specific attributes
    points: int = field(init=False)

    def __post_init__(self):
        for number in self.card_numbers:
            self.all_numbers[number] = True

        self.points = self._calculate_points()

    def get_number_of_matches(self) -> int:
        return sum(self.all_numbers[number] for number in self.winning_numbers)

    def _calculate_points(self) -> int:
        matches = self.get_number_of_matches()
        return 0 if matches == 0 else 1 << (matches - 1)
