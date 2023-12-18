from collections import namedtuple
from itertools import pairwise
from typing import List, Tuple

from advent_of_code_solver import BaseSolver

# An instruction is a tuple of (direction, metres, hex).
Instruction = namedtuple("Instruction", ("direction", "metres", "hex"))

# Directions
U = "U"
D = "D"
L = "L"
R = "R"

# Offsets for each direction in the complex plane.
OFFSETS = {
    U: -1,
    D: 1,
    L: -1j,
    R: 1j,
}

# Encoding for each direction.
ENCODING = [R, D, L, U]


def to_coord(complex_num: complex) -> tuple[int, int]:
    """
    Converts a coordinate represented as a complex number to (row, column) format.
    """
    return int(complex_num.real), int(complex_num.imag)


def determinant(r1: int, c1: int, r2: int, c2: int) -> int:
    """
    Calculates the determinant of a 2x2 matrix.
    """
    return r1 * c2 - r2 * c1


def get_num_interior_points(area: int, perimeter: int) -> int:
    """
    Uses Pick's theorem to calculate the number of interior points in a polygon.
    """
    return area - perimeter // 2 + 1


def get_coordinates(instructions: List[Instruction]) -> List[Tuple[int, int]]:
    """
    Converts a list of instructions to a list of coordinates.
    """
    # Use complex numbers to represent coordinates.
    curr = 0 + 0j
    coords = [to_coord(curr)]

    for direction, metres, _ in instructions:
        curr += OFFSETS[direction] * metres
        coords.append(to_coord(curr))

    return coords


def get_total_lagoon_area(instructions: List[Instruction]) -> int:
    """
    Calculates the total area of the lagoon, given a list of instructions.

    | Algorithm:
    | 1. Convert the instructions to a list of coordinates.
    | 2. Calculate the area of the polygon using the shoelace formula,
         and the perimeter by summing the instruction metres.
    | 3. Use Pick's theorem to calculate the number of interior points.
    | 4. The total area is the sum of the interior points and the perimeter.
    """
    coords = get_coordinates(instructions)
    perimeter = sum(instruction.metres for instruction in instructions)

    # Use the shoelace formula to calculate the area of the polygon.
    # The area is negated as calculating the area of a clockwise polygon gives a negative result.
    area = sum(determinant(*pair[0], *pair[1]) for pair in pairwise(coords))
    area = -area // 2

    interior_points = get_num_interior_points(area, perimeter)
    return interior_points + perimeter


def convert_instruction(instruction: Instruction) -> Instruction:
    """
    Extract the correct direction and metres from the hex value.
    """
    metres = int(instruction.hex[:-1], 16)
    direction = ENCODING[int(instruction.hex[-1])]
    return Instruction(direction, metres, None)


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []
        for line in file.read().splitlines():
            direction, metres, hex_value = line.split(" ")
            result.append(Instruction(direction, int(metres), hex_value[2:-1]))
        return result

    def solve_part1(self):
        return get_total_lagoon_area(self.input)

    def solve_part2(self):
        instructions = list(map(convert_instruction, self.input))
        return get_total_lagoon_area(instructions)
