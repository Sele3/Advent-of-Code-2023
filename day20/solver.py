from advent_of_code_solver import BaseSolver

from .utils import HIGH, LOW, Configuration, ModuleHandler


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []
        for line in file.read().splitlines():
            name, outputs = line.split(" -> ")
            result.append(Configuration(name, outputs))
        return ModuleHandler(result)

    def solve_part1(self):
        handler: ModuleHandler = self.input
        for _ in range(1000):
            handler.button_press()

        return handler.signals[LOW] * handler.signals[HIGH]

    def solve_part2(self):
        handler: ModuleHandler = self.input
        return handler.calculate_rx_presses_required()
