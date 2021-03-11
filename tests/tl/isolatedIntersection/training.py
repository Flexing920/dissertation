import os, sys, timeit

# import traci
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# constant define
GUI = True
CUR_DIR = os.getcwd()
INPUT_DIR = os.path.join(CUR_DIR, "data")
print(INPUT_DIR)
TRAIN_PATH = os.path.join(CUR_DIR, "train")
TEST_PATH = os.path.join(CUR_DIR, "test")
MODEL_PATH = os.path.join(CUR_DIR, "model")
SUMOCFG_FILE_NAME = "my.sumocfg"
MAX_STEPS = 300 # seconds

# network parameters
incoming_edge_ids = ["WC", "SC", "EC", "NC"]
outgoing_edge_ids = ["CW", "CS", "CE", "CN"]

# DQN parameters
EPISODES = 3

# define the phase index
PHASE_NS_GREEN = 0
PHASE_NS_YELLOW = 1
PHASE_EW_GREEN = 2
PHASE_EW_YELLOW = 3

class Simulation:

    def __init__(self, sumo_cmd, max_steps):
        self._sumo_cmd = sumo_cmd
        self._max_steps = max_steps
        self._step = 0
        self._cumulative_wait_store = []


    def run(self, episode):
        start_time = timeit.default_timer()
        traci.start(self._sumo_cmd)

        self._step = 0
        self._waiting_times = {}
        self._sum_waiting_time = 0
        self._sum_queue_length = 0
        old_total_waiting_time = 0

        print("Simulating...")
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            current_total_waiting_time = self.get_waiting_time(incoming_edge_ids)
            print(current_total_waiting_time)
            self._step += 1
        traci.close()
        simulation_time = round(timeit.default_timer() - start_time)
        print(f"Simulation time: {simulation_time}")

    def get_waiting_time(self, incoming_edges):
        car_ids = traci.vehicle.getIDList()
        for car_id in car_ids:
            waiting_time = traci.vehicle.getAccumulatedWaitingTime(car_id)
            edge_id = traci.vehicle.getRoadID(car_id)
            if edge_id in incoming_edge_ids:
                self._waiting_times[car_id] = waiting_time
            else:
                if car_id in self._waiting_times:
                    del self._waiting_times[car_id]
        total_waiting_time = sum(self._waiting_times.values())
        return total_waiting_time

    def get_queue_length(self, incoming_edges):
        # get the maximum queue length from each incoming lanes for the max-pressure method
        
class replay:
    pass

class DQN:
    pass

class DoubleDQN:
    pass

class DuelingDQN:
    pass

# helper functions
def set_sumo_cmd(GUI, INPUT_DIR, SUMOCFG_FILE_NAME, MAX_STEPS):
    # whether use gui 
    if GUI == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')


    # set the cmd for calling sumo
    cmd = [sumoBinary, "-c", os.path.join(INPUT_DIR, SUMOCFG_FILE_NAME),"--no-step-log", "true", "--waiting-time-memory", str(MAX_STEPS)]

    return cmd


if __name__ == "__main__":

    sumo_cmd = set_sumo_cmd(GUI, INPUT_DIR, SUMOCFG_FILE_NAME, MAX_STEPS)
    print(sumo_cmd)
    Simulation = Simulation(sumo_cmd, MAX_STEPS)

    episode = 0
    while episode < EPISODES:
        Simulation.run(episode)
        print(f"Check with episode: {episode}")
        episode += 1

    print("done")