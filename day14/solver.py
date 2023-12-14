from typing import Dict, List

from advent_of_code_solver import BaseSolver

from .utils import State, get_total_load, tilt_north

CYCLE_COUNT = 1_000_000_000


class Solver(BaseSolver):
    def parse_input(self, file):
        grid: List[List[str]] = list(map(list, file.read().splitlines()))
        return State(grid)

    def solve_part1(self):
        initial_state = self.input
        tilted_grid = tilt_north(initial_state.grid)
        return get_total_load(tilted_grid)

    def solve_part2(self):
        prev_state: State = self.input
        next_state: State = prev_state.cycle()

        # Stores a mapping of the state to its token.
        seen: Dict[State, int] = {prev_state: prev_state.token}
        # Since the tokens start from 0, we can use a list to store the states in order.
        states: List[State] = [prev_state]

        # Keep cycling until we find a state that we've seen before.
        while next_state not in seen:
            seen[next_state] = next_state.token
            states.append(next_state)
            next_state = next_state.cycle()

        # We find the cycle length by subtracting the token of the repeated state
        # from the token of its first occurrence.
        cycle_length = next_state.token - seen[next_state]

        # The target state is the state that we will reach after cycling the grid CYCLE_COUNT times.
        target_idx = seen[next_state] + (CYCLE_COUNT - seen[next_state]) % cycle_length
        target_state = states[target_idx]
        return get_total_load(target_state.grid)
