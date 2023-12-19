import re
from typing import List

from advent_of_code_solver import BaseSolver

from .utils import Part, PartMap, Rule, Workflow, WorkflowHandler

PART_RANGE = range(1, 4001)


def generate_workflows(s: str) -> List[Workflow]:
    """
    Format the input string into a list of workflows
    """
    result = []
    for line in s.splitlines():
        name, rules = re.match(r"(\w+)\{(.+)}", line).groups()
        rules = rules.split(",")

        default_rule = Rule("True", rules.pop())
        rules = [Rule(*rule.split(":")) for rule in rules]
        result.append(Workflow(name, rules, default_rule))
    return result


def generate_parts(s: str) -> List[Part]:
    """
    Format the input string into a list of parts
    """
    result = []
    for line in s.splitlines():
        x, m, a, s = map(int, re.findall(r"\d+", line))
        result.append(Part(x, m, a, s))
    return result


class Solver(BaseSolver):
    def parse_input(self, file):
        workflows, parts = file.read().split("\n\n")
        workflows = generate_workflows(workflows)
        parts = generate_parts(parts)
        return WorkflowHandler(workflows), parts

    def solve_part1(self):
        handler, parts = self.input
        accepted_parts = [part for part in parts if handler.evaluate_part(part)]
        return sum(accepted_parts)

    def solve_part2(self):
        handler, parts = self.input
        part_map = PartMap(PART_RANGE, PART_RANGE, PART_RANGE, PART_RANGE)
        return handler.count_accepted_combinations(part_map)
