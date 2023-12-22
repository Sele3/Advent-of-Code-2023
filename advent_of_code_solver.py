from abc import ABC, abstractmethod
from typing import TextIO


class BaseSolver(ABC):
    def __init__(self, input_file):
        self.input = None
        self.input_file = input_file

    def read_input_file(self):
        with open(self.input_file, "r") as file:
            self.input = self.parse_input(file)

    @abstractmethod
    def parse_input(self, file: TextIO):
        pass

    @abstractmethod
    def solve_part1(self):
        pass

    @abstractmethod
    def solve_part2(self):
        pass
