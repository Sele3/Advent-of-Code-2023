from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Set, Tuple


@dataclass
class Pipe(ABC):
    r: int
    c: int

    @abstractmethod
    def get_other_end(self, from_r: int, from_c: int) -> Tuple[int, int]:
        """
        Returns the coordinates of the other end of the pipe, given the coordinates of one end of the pipe
        """
        pass


class NSPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # Return the bottom end if coming from the top, otherwise return the top end
        return (self.r + 1, self.c) if from_r < self.r else (self.r - 1, self.c)


class EWPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # Return the right end if coming from the left, otherwise return the left end
        return (self.r, self.c + 1) if from_c < self.c else (self.r, self.c - 1)


class NEPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # Return the top end if coming from the right, otherwise return the right end
        return (self.r - 1, self.c) if from_r == self.r else (self.r, self.c + 1)


class NWPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # Return the top end if coming from the left, otherwise return the left end
        return (self.r - 1, self.c) if from_r == self.r else (self.r, self.c - 1)


class SEPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # Return the bottom end if coming from the right, otherwise return the right end
        return (self.r + 1, self.c) if from_r == self.r else (self.r, self.c + 1)


class SWPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # Return the bottom end if coming from the left, otherwise return the left end
        return (self.r + 1, self.c) if from_r == self.r else (self.r, self.c - 1)


class StartPipe(Pipe):
    def get_other_end(self, from_r: int, from_c: int):
        # We can assume that one end of the starting pipe is always pointing down
        return self.r + 1, self.c


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
