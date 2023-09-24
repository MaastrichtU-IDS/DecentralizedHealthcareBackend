from simulator import Simulator
from strategy.data_upload_strategy import DataUploadStrategy


def main():
    strategy = DataUploadStrategy()
    simulator = Simulator(3, strategy)
    simulator.run()


if __name__ == "__main__":
    main()
