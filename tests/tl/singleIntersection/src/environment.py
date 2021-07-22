from abc import ABCMeta, abstractmethod


import gym
from gym.spaces import Box
from gym.spaces import Tuple
from traci.exceptions import FatalTraCIError
from traci.exceptions import TraCIException

import sumolib

class Env(gym.Env, metaclass=ABCMeta):
    def __init__(self, env_params, sim_params, scenario=None):
        
        if scenario is not None:
            deprecated_attribute(self, "scenario", "network")
        self.network = scenario if scenario is not None else network
        

    def step(self, action):
        pass

    def render(self):
        pass

    def reset(self):
        pass
    