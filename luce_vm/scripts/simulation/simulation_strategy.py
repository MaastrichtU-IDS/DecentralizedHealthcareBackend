from abc import ABC, abstractmethod

# Define the Strategy interface
class SimulationStrategy(ABC):
    @abstractmethod
    def execute(self, simulator):
        pass


class DataUploadStrategy(SimulationStrategy):
    def execute(self, simulator):
        # 1. Clear user data
        simulator._clear_data()

        # 2. Register users
        simulator.register_users()

        # 3. Deploy registry
        simulator.deploy_registry()

        # 4. Upload data
        simulator.upload_data()

        # 5. Draw the graph
        simulator._draw_graph()