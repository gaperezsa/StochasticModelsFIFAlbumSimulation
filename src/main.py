
from simulation_config import SimualtionConfig
from simulator import Simulator

if __name__ == "__main__":
    config = SimualtionConfig()
    simulator = Simulator(config)
    simulator.simulate()
