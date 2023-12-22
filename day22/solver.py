import re
from collections import defaultdict, deque
from typing import Dict, List, Set

from advent_of_code_solver import BaseSolver

from .utils import Brick


def handle_falling(bricks: List[Brick]) -> None:
    """
    Handles the falling of bricks by updating the z_range of each brick.
    Also updates the supporting and supported_by attributes of each brick.
    """
    z_map: Dict[int, List[Brick]] = defaultdict(list)

    for brick in bricks:
        z_start, height = brick.z_range.start, len(brick.z_range)
        can_occupy = True

        while z_start > 1 and can_occupy:
            for curr in z_map[z_start - 1]:
                if not brick.positions.isdisjoint(curr.positions):
                    can_occupy = False
                    curr.supporting.add(brick)
                    brick.supported_by.add(curr)

            if can_occupy:
                z_start -= 1

        brick.z_range = range(z_start, z_start + height)
        for z in brick.z_range:
            z_map[z].append(brick)


def get_immovable_bricks(bricks: List[Brick]) -> Set[Brick]:
    """
    Returns the set of bricks that are immovable.
    A brick is immovable if it is supporting only one other brick.
    """
    immovable = set()

    for brick in bricks:
        if len(brick.supported_by) == 1:
            immovable |= brick.supported_by

    return immovable


# Constants used for the event queue
REMOVE = "remove"
ADD = "add"


def count_falling_bricks(brick: Brick):
    """
    Counts the number of bricks that will fall if the given brick is removed.
    The algorithm works by using a queue to simulate the bricks falling.
    All the remove events are handled first, and then subsequently handle all the add events.
    """
    event_queue = deque([(REMOVE, brick)])
    fall_count = 0

    while event_queue:
        event, curr = event_queue.popleft()

        if event == REMOVE:
            # Remove the current brick from the bricks that it is supporting
            for supporting in curr.supporting:
                supporting.supported_by.remove(curr)

                # If the brick is no longer supported, then it will fall, so add it to the event queue
                if not supporting.supported_by:
                    fall_count += 1
                    event_queue.appendleft((REMOVE, supporting))

            # After removing, append an add event to add the brick back to the bricks that it is supporting
            event_queue.append((ADD, curr))

        elif event == ADD:
            # Add the current brick back to the bricks that it is supporting
            for supporting in curr.supporting:
                supporting.supported_by.add(curr)

    return fall_count


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []
        for line in file.read().splitlines():
            x1, y1, z1, x2, y2, z2 = map(int, re.findall(r"\d+", line))

            positions = {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}
            z_range = range(z1, z2 + 1)

            result.append(Brick(positions, z_range))

        # Sort the bricks by their initial z value, so that the falling bricks can be processed in order
        return sorted(result, key=lambda brick: brick.z_range.start)

    def solve_part1(self):
        bricks: List[Brick] = self.input

        # Handle the falling of bricks
        handle_falling(bricks)

        # Get the set of immovable bricks
        immovable = get_immovable_bricks(bricks)

        # The number of bricks that can be safely removed is the number of bricks minus the number of immovable bricks
        return len(set(bricks) - immovable)

    def solve_part2(self):
        bricks: List[Brick] = self.input
        return sum(count_falling_bricks(brick) for brick in bricks)
