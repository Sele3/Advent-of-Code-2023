from dataclasses import dataclass, field
from typing import Set, Tuple


@dataclass
class Brick:
    """
    A brick is a collection of positions in the grid, and a range of z values
    """

    positions: Set[Tuple[int, int]]
    z_range: range

    # Used to keep track of which bricks are supporting this brick and which bricks this brick is supporting
    supporting: Set["Brick"] = field(init=False, default_factory=set)
    supported_by: Set["Brick"] = field(init=False, default_factory=set)

    def __repr__(self):
        return f"Brick({self.positions}, {self.z_range}, supporting={len(self.supporting)}, supported_by={len(self.supported_by)})"

    def __eq__(self, other):
        """
        Allows set operations to be performed on bricks
        """
        return self.positions == other.positions and self.z_range == other.z_range

    def __hash__(self):
        """
        Allows set operations to be performed on bricks
        """
        return hash((frozenset(self.positions), self.z_range))
