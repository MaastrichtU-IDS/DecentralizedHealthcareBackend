from simulator import Simulator
from simulation_strategy import DataUploadStrategy


def main():
    strategy = DataUploadStrategy()
    simulator = Simulator(3, strategy)
    simulator.run()


if __name__ == "__main__":
    main()

# strategy = DataUploadStrategy()
# simulator = Simulator(3, strategy)
# simulator.run_scenario()