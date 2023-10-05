from .base_strategy import SimulationStrategy


class DataAccessStrategy(SimulationStrategy):
    """
    1. Objectives:
    To simulate the conditions under which different entities (Healthcare Providers, Administrative Users, Third-party Researchers) access the shared healthcare data 
    while maintaining the anonymity and privacy of the patient and preserving the integrity and confidentiality of the data.
    """
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