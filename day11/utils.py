from bisect import bisect_left
from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Tuple


@dataclass
class GalaxyImage:
    """
    Represents a galaxy image, which is a grid of galaxies represented by "#" and empty space represented by "."
    """

    grid: List[str]
    times_larger: int = field(init=False, default=2)

    galaxy_coords: List[Tuple[int, int]] = field(init=False)
    empty_rows: List[int] = field(init=False)
    empty_cols: List[int] = field(init=False)

    def __post_init__(self):
        self.galaxy_coords = self._get_galaxy_coords()
        self.empty_rows = self._get_empty_rows(self.grid)
        self.empty_cols = self._get_empty_rows(list(map("".join, zip(*self.grid))))

    def calculate_total_path_distance(self) -> int:
        """
        Calculates the total path distance between all pairs of galaxies in the image.
        """
        all_combinations = combinations(self.galaxy_coords, 2)
        return sum(
            self._calculate_path_distance(start, end) for start, end in all_combinations
        )

    def _get_galaxy_coords(self):
        """
        Gets the coordinates of all galaxies in the image.
        """
        return [
            (i, j)
            for i, row in enumerate(self.grid)
            for j, c in enumerate(row)
            if c == "#"
        ]

    @staticmethod
    def _get_empty_rows(grid: List[str]) -> List[int]:
        """
        Gets the indices of all empty rows in the grid.
        """
        return [i for i, row in enumerate(grid) if all(c == "." for c in row)]

    def _calculate_path_distance(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> int:
        """
        Calculates the path distance between two galaxies.
        """
        r1, c1 = start
        r2, c2 = end

        extra_rows = abs(
            bisect_left(self.empty_rows, r2) - bisect_left(self.empty_rows, r1)
        )
        extra_cols = abs(
            bisect_left(self.empty_cols, c2) - bisect_left(self.empty_cols, c1)
        )

        return (
            abs(r2 - r1)
            + abs(c2 - c1)
            + (extra_rows + extra_cols) * (self.times_larger - 1)
        )
