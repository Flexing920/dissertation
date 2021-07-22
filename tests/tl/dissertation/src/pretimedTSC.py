import os
import sys
import argparse
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci
from src.environment import SumoEnvironment
from datetime import datetime

class pretimedTSC:
    def __init__(self, net_file, route_file):
        self.step = 0
        self.net_file = net_file 
        self.route_file = route_file
        print("pretimedTSC is called")

    def run(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            self.step += 1
        print(f"Simulation stops at {self.step}")
        traci.close()
        sys.stdout.flush()

