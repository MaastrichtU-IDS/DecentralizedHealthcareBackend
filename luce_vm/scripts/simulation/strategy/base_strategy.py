from abc import ABC, abstractmethod


# Define the Strategy interface
class SimulationStrategy(ABC):
    @abstractmethod
    def execute(self, simulator):
        pass