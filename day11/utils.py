from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Tuple


@dataclass
class GalaxyImage:
    """
    Represents a galaxy image, which is a grid of galaxies represented by "#" and empty space represented by "."
    """

    grid: List[str]

    # Number of times larger the empty space is
    times_larger: int = field(init=False, default=2)

    # Stores the coordinates of all galaxies in the image.
    galaxy_coords: List[Tuple[int, int]] = field(init=False)

    # Stores the row and column numbers of each galaxy in the image.
    row_numbers: List[int] = field(init=False)
    col_numbers: List[int] = field(init=False)

    # Stores the indices of all empty rows and columns in the image.
    empty_rows: List[int] = field(init=False)
    empty_cols: List[int] = field(init=False)

    def __post_init__(self):
        self.galaxy_coords = self._get_galaxy_coords()
        self.empty_rows = self._get_empty_rows(self.grid)
        self.empty_cols = self._get_empty_rows(list(map("".join, zip(*self.grid))))

        self._update_row_col_numbers()

    def set_times_larger(self, times_larger: int):
        """
        Sets the times larger value of the image.
        """
        self.times_larger = times_larger
        self._update_row_col_numbers()

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

        row_value1, row_value2 = self.row_numbers[r1], self.row_numbers[r2]
        col_value1, col_value2 = self.col_numbers[c1], self.col_numbers[c2]
        return abs(row_value2 - row_value1) + abs(col_value2 - col_value1)

    def _update_row_col_numbers(self):
        """
        Updates the row and column numbers of the image with the given times larger value.
        """
        # Initialize the row and column numbers to 1.
        self.row_numbers = [1] * len(self.grid)
        self.col_numbers = [1] * len(self.grid[0])

        # Set the empty rows and columns to the times larger value.
        # Then use prefix sums to calculate the row and column numbers.
        for empty_row in self.empty_rows:
            self.row_numbers[empty_row] = self.times_larger
        for r in range(1, len(self.row_numbers)):
            self.row_numbers[r] += self.row_numbers[r - 1]

        for empty_col in self.empty_cols:
            self.col_numbers[empty_col] = self.times_larger
        for c in range(1, len(self.col_numbers)):
            self.col_numbers[c] += self.col_numbers[c - 1]
