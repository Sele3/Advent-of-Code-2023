from dataclasses import dataclass, field
from typing import List


@dataclass
class ScratchCard:
    winning_numbers: List[int]
    card_numbers: List[int]

    # Solution-specific attributes
    points: int = field(init=False)

    def __post_init__(self):
        self.points = self._calculate_points()

    def get_number_of_matches(self) -> int:
        return len(set(self.winning_numbers) & set(self.card_numbers))

    def _calculate_points(self) -> int:
        matches = self.get_number_of_matches()
        return 0 if matches == 0 else 1 << (matches - 1)
