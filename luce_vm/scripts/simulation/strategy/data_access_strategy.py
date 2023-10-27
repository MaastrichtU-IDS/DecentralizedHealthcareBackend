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

        # 2. Register data providers
        simulator.register_users()

        # 3. Deploy registry
        simulator.deploy_registry()

        # 4. Upload data
        simulator.upload_data()

        # return
        # 5. Register data requesters
        simulator.register_requesters()

        # 6. Request access to data
        simulator.access_data()

        # 7. Draw the graph
        # simulator._draw_graph(name="data_access.png")
        simulator._save_graph(name="data_access.png")

        # 8. Analyze the graph
        simulator._analyze_graph()
