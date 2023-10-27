from simulator import Simulator
from strategy.data_upload_strategy import DataUploadStrategy
from strategy.data_access_strategy import DataAccessStrategy

# note:
# num_of_users must be greater than 1 because the simulator
# will pop the first user from the list as the admin user


def main():
    print("Simulation starts.")
    # print("1. Data upload strategy.")
    # # Case description: In this case, we simulate the data upload process in which a user uploads data to the system.
    # strategy = DataUploadStrategy()
    # simulator = Simulator(num_of_users=2, strategy=strategy)
    # simulator.run()

    print("2. Data access strategy.")
    # Case description: In this case, we simulate the data access process in which one user uploads data to the system and another user accesses the data.
    strategy = DataAccessStrategy()
    simulator = Simulator(num_of_users=2, strategy=strategy)
    simulator.run()


if __name__ == "__main__":
    main()
