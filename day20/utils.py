from abc import ABC, abstractmethod
from collections import deque, namedtuple
from dataclasses import dataclass, field
from math import lcm
from typing import Deque, Dict, List

# Constants for the signal values
HIGH = 1
LOW = 0

# Represents a configuration line from the input file
Configuration = namedtuple("Configuration", ("name", "outputs"))
# Represents a pulse of a signal
Pulse = namedtuple("Pulse", ("src", "dst", "signal"))


@dataclass
class Module(ABC):
    """
    Abstract base class for all modules.
    """

    name: str
    outputs: List[str] = field(init=False, default_factory=list)

    @abstractmethod
    def process_pulse(self, pulse: Pulse) -> List[Pulse]:
        """
        Process a pulse of a signal.
        :return: A list of pulses to be sent to the outputs of this module.
        """
        pass


@dataclass
class Broadcast(Module):
    """
    A module that broadcasts a pulse to all of its outputs.
    """

    def process_pulse(self, pulse: Pulse) -> List[Pulse]:
        return [Pulse(self.name, output, pulse.signal) for output in self.outputs]


class Receiver(Module):
    """
    A module that receives a pulse and does nothing with it.
    """

    def process_pulse(self, pulse: Pulse) -> List[Pulse]:
        return []


@dataclass
class FlipFlop(Module):
    """
    A module that flips the state of its output every time it receives a low pulse.
    """

    state: int = field(init=False, default=LOW)

    def process_pulse(self, pulse: Pulse) -> List[Pulse]:
        if pulse.signal == HIGH:
            return []

        self.state ^= 1
        return [Pulse(self.name, output, self.state) for output in self.outputs]


@dataclass
class Conjunction(Module):
    """
    A module that outputs a low pulse if all of its inputs are high, and a high pulse otherwise.
    """

    inputs: Dict[str, int] = field(init=False, default_factory=dict)

    def process_pulse(self, pulse: Pulse) -> List[Pulse]:
        self.inputs[pulse.src] = pulse.signal
        signal = LOW if all(self.inputs.values()) else HIGH
        return [Pulse(self.name, output, signal) for output in self.outputs]

    def add_input(self, name: str) -> None:
        """
        Add an input to this conjunction.
        """
        self.inputs[name] = LOW


class ModuleHandler:
    """
    A class that handles the modules and their signals.
    """

    BUTTON_PRESSES = 0

    def __init__(self, configurations: List[Configuration]):
        self.modules = {}
        self.signals = {LOW: 0, HIGH: 0}
        self._build_modules(configurations)

        # For part 2, we need to keep track of the pulses that we have sent to the module named rx.
        self.pulse_tracker = PulseTracker()

    def button_press(self) -> None:
        """
        Simulate a button press. An initial low pulse is sent to the broadcaster module,
        and the pulse is propagated through the modules.
        """
        q: Deque[Pulse] = deque()
        q.append(Pulse(None, "broadcaster", LOW))

        ModuleHandler.BUTTON_PRESSES += 1

        while q:
            # Process the next pulse in the queue
            pulse = q.popleft()
            self.signals[pulse.signal] += 1

            # Notify the pulse tracker of the current pulse
            self.pulse_tracker.notify(pulse)

            # Send the pulse to the destination modules
            for pulse in self.modules[pulse.dst].process_pulse(pulse):
                q.append(pulse)

    def calculate_rx_presses_required(self) -> int:
        """
        Calculate the minimum number of button presses required to deliver a single low pulse to the 'rx' module.

        The 'rx' module is connected to the conjunction module named 'nc'.
        The result is the LCM of the number of button presses required for each of its inputs to send a low pulse.
        """
        conjunction: Conjunction = self.modules["nc"]
        # Initialise the pulse tracker with the pulses that we need to track
        for src in conjunction.inputs:
            self.pulse_tracker.track_pulse(Pulse(src, "nc", HIGH))

        # Simulate button presses until all the pulses have been tracked
        while not self.pulse_tracker.all_pulses_tracked():
            self.button_press()

        # Calculate the least common multiple of the tracked pulses
        return self.pulse_tracker.calculate_lcm()

    def _build_modules(self, configurations: List[Configuration]) -> None:
        """
        Helper function to build the modules from the configurations.
        """
        conjunctions: Dict[str, Conjunction] = {}

        # First, add all the modules to the dictionary
        for config in configurations:
            mtype, name = config.name[0], config.name[1:]
            match mtype:
                case "%":
                    self.modules[name] = FlipFlop(name)
                case "&":
                    conjunctions[name] = self.modules[name] = Conjunction(name)
                case "b":
                    self.modules["broadcaster"] = Broadcast("broadcaster")

        # Then, add the outputs to each of the modules
        for config in configurations:
            name = config.name if config.name[0] == "b" else config.name[1:]
            self.modules[name].outputs = config.outputs.split(", ")

            for output in self.modules[name].outputs:
                # If the output is not a module, create a receiver for it
                if output not in self.modules:
                    self.modules[output] = Receiver(output)
                # If the output is a conjunction, add the name of the current module as an input
                if output in conjunctions:
                    conjunctions[output].add_input(name)


@dataclass
class PulseTracker:
    """
    A class that keeps track of the pulses that we need to track for part 2.
    """

    # The pulses that we need to track
    tracked: set[Pulse] = field(init=False, default_factory=set)
    # The number of button presses needed before the tracked pulse is sent
    tracked_counts: dict[Pulse, int] = field(init=False, default_factory=dict)

    def track_pulse(self, pulse: Pulse) -> None:
        self.tracked.add(pulse)

    def notify(self, pulse: Pulse) -> None:
        if pulse in self.tracked:
            self.tracked_counts[pulse] = ModuleHandler.BUTTON_PRESSES
            self.tracked.remove(pulse)

    def all_pulses_tracked(self) -> bool:
        return len(self.tracked) == 0

    def calculate_lcm(self) -> int:
        return lcm(*self.tracked_counts.values())
