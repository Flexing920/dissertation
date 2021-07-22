import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    from sumolib import checkBinary
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import sumolib
import numpy as np
from networkdata import NetworkData

import re

if __name__ == "__main__":
    
    cfg1 = "../networks/grid2/my.sumocfg"
    cfg2 = "../networks/single_intersection/sumo.sumocfg"
    port = 9000
    port1 = 9000 + 1
    port2 = 9000 + 2

    print(f"port1 is {port1}")
    print(f"port2 is {port2}")

    traci.start(["sumo", "-c", cfg1], port=port1, label="sim1")
    traci.start(["sumo", "-c", cfg2], port=port2, label="sim2")
    conn1 = traci.getConnection("sim1")
    conn2 = traci.getConnection("sim2")

    trafficlights1 = conn1.trafficlight.getIDList()
    print(trafficlights1[0], trafficlights1[-1])
    s1 = ""
    # trafficlights1.sort()
    trafficlights2 = conn2.trafficlight.getIDList()
    print(trafficlights1)
    step = 0
    while step <= 5:
        traci.switch("sim1")
        traci.simulationStep() # run 1 step for sim1
        traci.switch("sim2")
        traci.simulationStep()
        if step == 3:
            print(f"step == 3 and {trafficlights1}")
        if step == 4:
            print(f"step == 4 and {trafficlights2[0]}")
        step += 1
    traci.switch("sim1")
    traci.close()
    traci.switch("sim2")
    traci.close()



