import os, sys, timeit, random

# import traci
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# import modules for keras
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'  # kill warning about tensorflow
import tensorflow as tf
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import load_model


# constant define
GUI = False
CUR_DIR = os.getcwd()
INPUT_DIR = os.path.join(CUR_DIR, "data")
print(INPUT_DIR)
TRAIN_PATH = os.path.join(CUR_DIR, "train")
TEST_PATH = os.path.join(CUR_DIR, "test")
MODEL_PATH = os.path.join(CUR_DIR, "model")
SUMOCFG_FILE_NAME = "my.sumocfg"
MAX_STEPS = 300 # seconds

# network parameters
trafficLightID = "C"
incoming_edge_ids = ["WC", "SC", "EC", "NC"]
outgoing_edge_ids = ["CW", "CS", "CE", "CN"]

# needs to define a dictionary where maps the incoming to outgoing edges


# DQN parameters
EPISODES = 3

# define the phase index
PHASE_NS_GREEN = 0
PHASE_NS_YELLOW = 1
PHASE_EW_GREEN = 2
PHASE_EW_YELLOW = 3

# only two actions at this moment
ACTIONS = [0, 2]


class Simulation:

    def __init__(self, sumo_cmd, max_steps, tlsID, model):
        self._sumo_cmd = sumo_cmd
        self._max_steps = max_steps
        self._step = 0
        self._cumulative_wait_store = []
        self._model = model
        self._tlsID = tlsID


    def run(self, episode, incoming_edges):
        start_time = timeit.default_timer()
        traci.start(self._sumo_cmd)

        self._step = 0
        self._waiting_times = {}
        self._sum_waiting_time = 0
        self._sum_queue_length = 0
        old_total_waiting_time = 0

        print("Simulating...")
        while traci.simulation.getMinExpectedNumber() > 0:
            # # get all laneID information
            # if self._step == 0:
            #     for edgeID in incoming_edges:
            #         for laneID in self.get_laneIDs(edgeID):
            #             self.get_lane_direction(laneID)

            traci.simulationStep()
            current_total_waiting_time = self.get_waiting_time(incoming_edge_ids)
            # print(current_total_waiting_time)
            # testLaneID = "EC_1"
            # print(traci.lane.getLastStepHaltingNumber(testLaneID))
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

    def get_laneIDs(self, edgeID):
        laneIDs = []
        numOfLanes = traci.edge.getLaneNumber(edgeID)
        for i in range(numOfLanes):
            laneIDs.append(f"{edgeID}_{i}")
        return laneIDs

    def get_lane_direction(self, laneID):
        # hard coding at this moment since I didn't find the function to tell the direction of each lane
        # It can be done by adding another static function in Lane.h/.cpp later
        pass
    
    def get_incoming_lane_queue_length(self, incoming_edges):
        # get the max queue length from all directions
        # normally has 8 different directions
        # here we only consider 4 without considering left turning
        # use a dictionary to keep track of the queuing number vehicles in each phase
        # all phases: EW,EWL...  where L means left turn vehicles 
        pass
    
    

    def get_max_pressure_direction(self, incoming_edges, outgoing_edges):
        # we can calculate the sum of pressure from two phases where they can be allowed at the same time for more flexibility
        pass
    
    # get sum of queue length from all directions
    def get_queue_length(self, incoming_edges):
        queue_length = 0
        for edgeID in incoming_edges:
            queue_length += traci.edge.getLastStepHaltingNumber(edgeID)
        return queue_length
        
    def get_state(self, incoming_edges, outgoing_edges):
        states = {}
        for edgeID in incoming_edges:
            states[edgeID] = traci.edge.getLastStepHaltingNumber(edgeID)
        for edgeID in outgoing_edges:
            states[edgeID] = traci.edge.getLastStepHaltingNumber(edgeID)
        return states
        
        # return the number of vehicles that stopped at each directions for both incoming and outgoing edges
        # later we can consider the stopped vehicles for each lane

    def choose_action(self, state, epsilon, ACTIONS):
        if random.random() < epsilon:
            return random.choice(ACTIONS)
        else:
            # predict_one is not implemented yet
            # the return of precict_one should be an integer representing the phase index
            return np.argmax(self._model.predict_one(state))

    def set_green_phase(self, action):
        traci.trafficlight.setPhase(self._tlsID, action)

    def set_yellow_phase(self, cur_action, new_action):
        if cur_action != new_action:
            # we have to define the phase in this way to use below method to call yellow phase
            traci.trafficlight.setPhase(self._tlsID, cur_action + 1)

    def get_current_action(self):
        return traci.trafficlight.getPhase(self._tlsID)
            
class replay:
    def __init__(self, max_size, min_size, input_shape):
        self._mem_size_max = max_size
        self._mem_size_min = min_size
        self._mem_counter = 0
        # input_shape is not using at this moment
        self._experiences = []

    # add experince
    def add_experience(self, experience):
        self._experiences[self._mem_counter % self._mem_size_max] = experience
        self._mem_counter += 1


    # helper func: get current experiences size
    def _get_current_size(self):
        return len(self._experiences)

    # experience replay without priority
    def get_experiences(self, n):
        # not enough experiences and no experience replay
        if self._get_current_size() < slef._mem_size_min:
            return []

        # get all current experiences when not enough for n
        if n > self._get_current_size():
            return random.sample(self._experiences, self._get_current_size())

        # get n random experiences
        else:
            return random.sample(self._experiences, n)

    def get_experiences_priority(self, n):
        pass

class ModelTrain:
    def __init__(self, num_layers, num_nodes, batch_size, learning_rate, input_dim, out_dim):
        self._input_dim = input_dim


class ModelTest:
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
    # print(sumo_cmd)
    # needs to implement the model and add model parameter here
    Simulation = Simulation(sumo_cmd, MAX_STEPS, trafficLightID)

    episode = 0
    while episode < EPISODES:
        Simulation.run(episode, incoming_edge_ids)
        print(f"Check with episode: {episode}")
        episode += 1

    print("done")