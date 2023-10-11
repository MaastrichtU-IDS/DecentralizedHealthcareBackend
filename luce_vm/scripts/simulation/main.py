from simulator import Simulator
from strategy.data_upload_strategy import DataUploadStrategy
from strategy.data_access_strategy import DataAccessStrategy


def main():
    strategy = DataAccessStrategy()
    # simulator = Simulator(3, strategy)
    simulator = Simulator(num_of_users=2, strategy=strategy)
    simulator.run()


if __name__ == "__main__":
    main()
