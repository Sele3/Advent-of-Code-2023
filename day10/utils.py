from abc import ABC
from dataclasses import dataclass, field
from typing import List, Set, Tuple


class Pipe(ABC):
    def __init__(self, r: int, c: int, dr1: int, dc1: int, dr2: int, dc2: int):
        self.r = r
        self.c = c
        self.pipe_end1 = (r + dr1, c + dc1)
        self.pipe_end2 = (r + dr2, c + dc2)

    def get_other_end(self, from_r: int, from_c: int) -> Tuple[int, int]:
        """
        Returns the coordinates of the other end of the pipe, given the coordinates of one end of the pipe
        """
        return self.pipe_end1 if (from_r, from_c) == self.pipe_end2 else self.pipe_end2


class NSPipe(Pipe):
    def __init__(self, r: int, c: int):
        # Top end and bottom end
        super().__init__(r, c, -1, 0, 1, 0)


class EWPipe(Pipe):
    def __init__(self, r: int, c: int):
        # Left end and right end
        super().__init__(r, c, 0, -1, 0, 1)


class NEPipe(Pipe):
    def __init__(self, r: int, c: int):
        # Top end and right end
        super().__init__(r, c, -1, 0, 0, 1)


class NWPipe(Pipe):
    def __init__(self, r: int, c: int):
        # Top end and left end
        super().__init__(r, c, -1, 0, 0, -1)


class SEPipe(Pipe):
    def __init__(self, r: int, c: int):
        # Bottom end and right end
        super().__init__(r, c, 1, 0, 0, 1)


class SWPipe(Pipe):
    def __init__(self, r: int, c: int):
        # Bottom end and left end
        super().__init__(r, c, 1, 0, 0, -1)


class StartPipe(Pipe):
    def __init__(self, r: int, c: int):
        # We can assume that one end of the starting pipe is always pointing down
        super().__init__(r, c, 0, 0, 1, 0)


PIPES = {
    "│": NSPipe,
    "─": EWPipe,
    "└": NEPipe,
    "┘": NWPipe,
    "┌": SEPipe,
    "┐": SWPipe,
    "S": StartPipe,
}


@dataclass
class PipeField:
    grid: List[str]
    start_r: int
    start_c: int

    # Contains the coordinates of the main pipe loop
    main_loops: Set[Tuple[int, int]] = field(default_factory=set)

    def __post_init__(self):
        self.main_loops.add((self.start_r, self.start_c))
        self._traverse()

    def _traverse(self):
        """
        Traverses the pipe field and finds the main pipe loop
        """
        pipe: Pipe = StartPipe(self.start_r, self.start_c)
        prev_r, prev_c = self.start_r, self.start_c
        next_r, next_c = pipe.get_other_end(prev_r, prev_c)

        # Traverse the pipe field until we reach the starting pipe again
        while (next_r, next_c) != (self.start_r, self.start_c):
            self.main_loops.add((next_r, next_c))
            pipe = PIPES[self.grid[next_r][next_c]](next_r, next_c)
            next_r, next_c = pipe.get_other_end(prev_r, prev_c)
            prev_r, prev_c = pipe.r, pipe.c

        # Replace the starting pipe with a pipe that points in the correct direction
        if prev_c == self.start_c:
            start_replacement = "│"
        elif prev_r > self.start_r:
            start_replacement = "┌"
        else:
            start_replacement = "┐"
        self.grid[self.start_r] = self.grid[self.start_r].replace(
            "S", start_replacement
        )

    def get_enclosed_area(self) -> int:
        """
        Returns the area enclosed by the main pipe loop

        | Intuition:
        | - The tiles enclosed by the main pipe will have an odd parity,
            when counting the number of vertical pipes to the left
        | - "|", "┌┘", and "└┐" are considered vertical pipes and will change the parity
        | - We can track the previous bent pipe to determine if the current bent pipe is a combination of "┌┘" or "└┐"
        """
        area = 0

        for r, row in enumerate(self.grid):
            parity = 0
            prev_bent_pipe = ""

            for c, cell in enumerate(row):
                if (r, c) in self.main_loops:
                    # Flip the parity if we encounter a vertical pipe or a combination of "┌┘" or "└┐"
                    if cell == "│" or prev_bent_pipe + cell in {"┌┘", "└┐"}:
                        parity ^= 1

                    # Track the previous bent pipe
                    if cell in {"└", "┘", "┐", "┌"}:
                        prev_bent_pipe = cell

                    continue

                # The tile is enclosed if it's not part of the main pipe loop and has odd parity
                elif parity == 1:
                    area += 1

        return area
