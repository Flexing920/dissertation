from dqn_model import TrainModel
from replay import ReplayBuffer
import numpy as np


import os, sys, timeit, random
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # kill GPU warning info
# import traci
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


# constant parameters
# to trigger the yellow transition phase, call action + number of action_space
# here is 2, so action + self.action_space for corresponding yellow phase
PHASE_NS_GREEN = 0
PHASE_EW_GREEN = 1
PHASE_NS_YELLOW = 2
PHASE_EW_YELLOW = 3
# needs to change the tls definition in the network

class Agent:
    def __init__(self, Model, Memory, sumocfg_cmd, gamma, states, actions, epsilon, batch_size, input_dims, epsilon_dec = 1e-3, epsilon_min = 0.01, max_mem_size = 50000, min_mem_size, fname="dqn_model.h5", learning_rate, n_layers, n_nodes, min_green=6, max_green=99, yellow_duration=3, max_steps, epochs, junctionID):
        self.num_states = states # an int for number of states, 8 for this case
        self.num_actions = actions # an int for number of all available green phases, [0,2]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.model_file = fname
        self.junctionID = junctionID

        self.memory = ReplayBuffer(max_mem_size, input_dims)
        self.model = TrainModel(n_layers, n_nodes, batch_size, learning_rate, input_dims, actions)

        self.sumocfg_cmd = sumocfg_cmd
        self.step = 0
        self.min_green = min_green
        self.max_green = max_green
        self.yellow_duration = yellow_duration
        self.max_steps = max_steps
        self.epochs = epochs

        self.reward_track = []
        self.cumulative_wait_track = []

    def run(self):
        start_time = timeit.default_timer()

        traci.start(self.sumocfg_cmd)
        print("Starting simulation...")

        # init
        self.step = 0
        self.waiting_time = {}
        self.sum_reward = 0
        self.sum_queue_length = 0
        self.sum_waiting_time = 0
        old_total_wait = 0
        old_state = -1
        odl_action = -1

        while self.step < self.max_steps:
            # get the queue length from all incoming and outgoing edges
            current_state = self.get_state()
            current_total_wait = self.get_total_waiting_time()
            reward = old_total_wait - current_total_wait
            
            if self.step != 0:
                self.memory.store_transition(old_state, old_action, reward, current_state)
            
            action = self.choose_action(current_state)

            if self.step != 0 and old_action != action:
                self.set_yellow_phase(old_action)
                self.simulate(self.yellow_duration)

            self.set_green_phase(action)
            self.simulate(self.min_green)

            old_state = current_state
            old_action = action
            old_total_wait = current_total_wait

            if reward < 0:
                self.sum_reward += reward

        self.save_episode_stats()

        print(f"Total reward:{self.sum_reward}, - Epsilon: {round(self.epsilon, 2)}")

        traci.close()
        simulation_time = round(timeit.default_timer() - start_time, 1)

        print("Training...")
        start_time = timeit.default_timer()
        for _ in range(self.epochs):
            self.learn()
        training_time = round(timeit.default_timer - start_time, 1)

        return simulation_time, training_time
        

    
    def simulate(self, step_todo):
        if (self.step + step_doto) >= self.max_steps:
            step_todo = self.max_steps - self.step

        while step_todo > 0:
            traci.simulationStep()
            self.step += 1
            step_todo -= 1
            queue_length = self.get_queue_length()
            self.sum_queue_length += queue_length
            self.sum_waiting_time += queue_length


    def store_memory(self, state, action, reward, state_):
        self.memory.store_transition(state, action, reward, state_)

    def choose_action(self, observation):
        if random.random() < self.epsilon:
            action = random.randint(0, self.num_actions - 1)
        else:
            state = np.array([observation])
            action = np.argmax(actions)
        return action

    def set_yellow_phase(self, action):
        traci.trafficlight.setPhase(self.junctionID, action+self.num_actions)

    def set_green_phase(self, action_index):
        if action_index == 0:
            traci.trafficlight_setPhase(self.junctionID, PHASE_NS_GREEN)
        elif action_index == 1:
            traci.trafficlight_setPhase(self.junctionID, PHASE_EW_GREEN)
    
    def get_state(self):
        """
        state represent the number of vehicles in the queue of each incoming and outgoing lanes. For current scenario,there are 8 integer in the state. The format is [incoming 1, outgoing 1, incoming 2, outgoing 2, ...]
        N north ...
        C center
        pattern: north, east, south, west
        """
        # get the queue from each lane and choose the max for that approach
        queue_NC = max(traci.lane.getLastStepLength("NC_0"), traci.lane.getLastStepLength("NC_1"))
        queue_CS = max(traci.lane.getLastStepLength("CS_0"), traci.lane.getLastStepLength("CS_1"))
        queue_EC = max(traci.lane.getLastStepLength("EC_0"), traci.lane.getLastStepLength("EC_1"))
        queue_CW = max(traci.lane.getLastStepLength("CW_0"), traci.lane.getLastStepLength("CW_1"))
        queue_SC = max(traci.lane.getLastStepLength("SC_0"), traci.lane.getLastStepLength("SC_1"))
        queue_CN = max(traci.lane.getLastStepLength("CN_0"), traci.lane.getLastStepLength("CN_1"))
        queue_WC = max(traci.lane.getLastStepLength("WC_0"), traci.lane.getLastStepLength("WC_1"))
        queue_CE = max(traci.lane.getLastStepLength("CE_0"), traci.lane.getLastStepLength("CE_1"))
        return [queue_NC, queue_CS, queue_EC, queue_CW, queue_SC, queue_CN, queue_WC, queue_CE]

    def get_queue_length(self):
        # only consider the incoming queue length
        sum = 0 
        temp = self.get_state()
        for i in range(len(temp)):
            if i % 2 == 0:
                sum += temp[i]
        return sum

    def get_total_waiting_time(self):
        incoming_edges = ["NC", "EC", "SC", "WC"]

        carIDs = traci.vehicle.getIDList()
        for carID in carIDs:
            wait = traci.vehicle.getAccumulateWaitingTime(carID)
            edge_id = traci.vehicle.getRoadID(carID)
            if edge_id in incoming_edges:
                self.waiting_time[carID] = wait
            else:
                if carID in self.waiting_time:
                    del self.waiting_time[carID]
        total_wait = sum(self.waiting_time.values())
        return total_wait

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return
        
        states, actions, rewards, states_ = \
            self.memory.sample_buffer(self.batch_size)

        q_eval = self.model.predict_batch(states)
        q_next = self.model.predict_batch(states_)

        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        
        q_target[batch_index, actions] = rewards + self.gamma * np.max(q_next, axis=1)

        self.model.train_batch(states, q_target)

        self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > \
            self.epsilon_min else self.epsilon_min
        
    def save_episode_stats(self):
        self.reward_track.append(self.reward_sum)
        self.cumulative_wait_track.append(self.sum_waiting_time)
    
    @property
    def reward_track(self):
        return self.reward_track
    
    @property
    def cumulative_wait_track(self):
        return self.cumulative_wait_track


